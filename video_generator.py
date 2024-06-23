import os
from moviepy.editor import (
    ImageClip, AudioFileClip, TextClip, CompositeVideoClip,
    vfx, concatenate_videoclips
)
from moviepy.editor import TextClip
TextClip.list('color')
from pydub import AudioSegment
from textwrap import wrap
from .video_configs import (
    FPS, BRIGHTNESS_FACTOR, SPEED_FACTOR,
    TITLE_FONTSIZE, TITLE_FONT, TITLE_COLOR,
    TITLE_POSITION, TITLE_MAX_CHARS_PER_LINE, SUBTITLE_FONTSIZE,
    SUBTITLE_FONT, SUBTITLE_COLOR, SUBTITLE_POSITION,
    SUBTITLE_MAX_CHARS_PER_LINE, CHUNK_DURATION, TITLE_STROKE_COLOR,
    TITLE_METHOD, SUBTITLE_METHOD, SUBTITLE_STROKE_COLOR, TITLE_STROKE_WIDTH, SUBTITLE_STROKE_WIDTH,
    TITLE_BG_COLOR, SUBTITLE_BG_COLOR,
    
    BG_BRIGHTNESS_FACTOR, THUMBNAIL_TITLE_FONTSIZE, THUMBNAIL_TITLE_MAX_CHARS_PER_LINE, THUMBNAIL_TITLE_FONT
    , THUMBNAIL_TITLE_COLOR, THUMBNAIL_TITLE_STROKE_COLOR, THUMBNAIL_TITLE_BG_COLOR, THUMBNAIL_TITLE_METHOD
    , THUMBNAIL_TITLE_POSITION, THUMBNAIL_TITLE_STROKE_WIDTH, THUMBNAIL_CLIP_DURATION
)

def split_news_script_into_chunks(text: str, audio_duration: int) -> list:
    """
    Split new text into chunks of a specified size.

    Args:
        text (str): Text to split.
        chunk_size (int, optional): Number of words per chunk. Defaults to 7.

    Returns:
        list: List of text chunks.
    """
    # Calculate the number of chunks
    num_chunks = int(audio_duration // CHUNK_DURATION)

    # Split the text into the calculated number of chunks
    words = text.split()
    chunk_size = len(words) // num_chunks + (len(words) % num_chunks > 0)
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def create_subtitle_clips(text: str, title: str, duration: float) -> list:
    """
    Create subtitle clips from text, split into chunks, ensuring each chunk fits within the frame.

    Args:
        text (str): Text to display as subtitles.
        duration (float): Duration of the audio.
        chunk_size (int, optional): Number of words per subtitle chunk. Defaults to 7.

    Returns:
        list: List of subtitle clips.
    """

    chunks = split_news_script_into_chunks(text, duration)


    subtitle_clips = []
    # Create the title clip with bold font and larger size with shadow
    wrapped_title = "\n".join(wrap(title, TITLE_MAX_CHARS_PER_LINE))
    title_clip = TextClip(
    wrapped_title,
    fontsize=TITLE_FONTSIZE,
    font=TITLE_FONT,
    color=TITLE_COLOR,
    method=TITLE_METHOD,
    stroke_color=TITLE_STROKE_COLOR,
    stroke_width=TITLE_STROKE_WIDTH,  # Width of the stroke for outline effect
    bg_color = TITLE_BG_COLOR
    ).set_position(TITLE_POSITION, relative=True).set_duration(duration)

    # subtitle_clips.append(title_shadow)
    subtitle_clips.append(title_clip)

    for i, chunk in enumerate(chunks):
        wrapped_text = "\n".join(wrap(chunk, SUBTITLE_MAX_CHARS_PER_LINE))
        clip_duration = CHUNK_DURATION if i < len(chunks) - 1 else duration - (i * CHUNK_DURATION)
        
        subtitle_clip = TextClip(
            wrapped_text,
            font=SUBTITLE_FONT,
            fontsize=SUBTITLE_FONTSIZE,
            color=SUBTITLE_COLOR,
            stroke_color=SUBTITLE_STROKE_COLOR,
            stroke_width=SUBTITLE_STROKE_WIDTH,  # Width of the stroke for outline effect            
            method=SUBTITLE_METHOD,
            bg_color = SUBTITLE_BG_COLOR
        ).set_position(SUBTITLE_POSITION, relative=True).set_duration(clip_duration).set_start(i * CHUNK_DURATION)

        # subtitle_clips.append(subtitle_shadow)
        subtitle_clips.append(subtitle_clip)

    return subtitle_clips


def create_thumbnail(image_path, title_text):
    """
    Creates a thumbnail with the specified title text overlaid on the image.

    :param image_path: Path to the input image
    :param title_text: Text to overlay on the image
    :return: Thumbnail ImageClip
    """
    # Load the image
    image_clip = ImageClip(image_path)
    image_clip = image_clip.fx(vfx.colorx, BG_BRIGHTNESS_FACTOR)

    # Create the text clip
    wrapped_title = "\n".join(wrap(title_text, THUMBNAIL_TITLE_MAX_CHARS_PER_LINE))
    title_clip = TextClip(
    wrapped_title,
    fontsize=THUMBNAIL_TITLE_FONTSIZE,
    font=THUMBNAIL_TITLE_FONT,
    color=THUMBNAIL_TITLE_COLOR,
    method=THUMBNAIL_TITLE_METHOD,
    stroke_color=THUMBNAIL_TITLE_STROKE_COLOR,
    stroke_width=THUMBNAIL_TITLE_STROKE_WIDTH,  # Width of the stroke for outline effect
    bg_color = THUMBNAIL_TITLE_BG_COLOR
    ).set_position(THUMBNAIL_TITLE_POSITION, relative=True)

    # Combine the image and text clips
    composite_clip = CompositeVideoClip([image_clip, title_clip])

    return composite_clip



def create_video_clip(item: dict, fps: int = FPS, brightness_factor: float = BRIGHTNESS_FACTOR) -> CompositeVideoClip:
    """
    Create a video clip (audio attached) from a JSON item.

    Args:
        item (dict): JSON item containing 'title', 'audio', 'frame', and 'news'.
        fps (int, optional): Frames per second for the video. Defaults to 24.

    Returns:
        CompositeVideoClip: Video clip with subtitles.
    """
    audio = AudioSegment.from_file(item['audio'])
    audio_duration = len(audio) / 1000.0

    frame_clip = ImageClip(item['frame']).set_duration(audio_duration)
    audio_clip = AudioFileClip(item['audio'])

    video_clip = frame_clip.set_audio(audio_clip)

    # Reduce brightness
    video_clip = video_clip.fx(vfx.colorx, brightness_factor)

    subtitle_clips = create_subtitle_clips(item['news'], item['title'], audio_duration)

    # Create thumbnail
    thumbnail_clip = create_thumbnail(item['frame'], item['title']).set_duration(THUMBNAIL_CLIP_DURATION)
    # Combine thumbnail and video clips
    final_video_clip = concatenate_videoclips([thumbnail_clip, CompositeVideoClip([video_clip, *subtitle_clips])])

    return final_video_clip
    # return CompositeVideoClip([video_clip, *subtitle_clips])





def combine_clips(clips: list) -> CompositeVideoClip:
    """
    Combine a list of video clips into a single video clip.

    Args:
        clips (list): List of video clips.

    Returns:
        CompositeVideoClip: Combined video clip.
    """
    return concatenate_videoclips(clips)

def postprocess_clip(clip: CompositeVideoClip, speed_factor: float = SPEED_FACTOR) -> CompositeVideoClip:
    """
    Apply postprocessing effects to a video clip, such as adjusting speed.

    Args:
        clip (CompositeVideoClip): Video clip to process.
        speed_factor (float, optional): Factor to speed up the video. Defaults to 1.2.

    Returns:
        CompositeVideoClip: Postprocessed video clip.
    """
    return clip.fx(vfx.speedx, factor=speed_factor)

def save_video(clip: CompositeVideoClip, output_video_path: str, output_thumbnail_path: str, fps: int = FPS):
    """
    Save the video clip to a file.

    Args:
        clip (CompositeVideoClip): Video clip to save.
        output_video_path (str): Path to save the final video.
        fps (int, optional): Frames per second for the video. Defaults to 12.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    # Save the thumbnail as an image
    clip.save_frame(output_thumbnail_path, t=0)
    clip.write_videofile(output_video_path, fps=fps, codec="libx264", audio_codec="aac")
    print(f"Video saved to {output_video_path} and thumbnail {output_thumbnail_path}")

# def process_video_clips(clips: list, output_path: str, fps: int = FPS, speed_factor: float = SPEED_FACTOR):
#     """
#     Process and export the final video by concatenating clips, adjusting speed, and brightness.

#     Args:
#         clips (list): List of video clips.
#         output_path (str): Path to save the final video.
#         fps (int, optional): Frames per second for the video. Defaults to 12.
#         speed_factor (float, optional): Factor to speed up the video. Defaults to 1.2.
#         brightness_factor (float, optional): Factor to adjust brightness. Defaults to 0.6.
#     """

#     final_clip = final_clip.fx(vfx.speedx, factor=speed_factor)
#     final_clip.write_videofile(output_path, fps=fps, codec="libx264", audio_codec="aac")
#     print(f"Video saved to {output_path}")





# ---------------- ANOTHER STABLE VERSION ----------------------
    # TITLE_FONTSIZE = 34
    # TITLE_FONT = 'Arial-Bold'
    # TITLE_COLOR = 'white'
    # TITLE_STROKE_COLOR = 'orange'
    # TITLE_POSITION = (0, 0.10)
    # TITLE_MAX_CHARS_PER_LINE = 35
    # TITLE_SIZE = (1028, None)  # Video size for caption method
    # TITLE_MAX_CHARS_PER_LINE = 30


    # # Create the title clip with bold font and larger size with shadow
    # wrapped_title = "\n".join(wrap(title, TITLE_MAX_CHARS_PER_LINE))
    # title_clip = TextClip(
    # wrapped_title,
    # fontsize=TITLE_FONTSIZE,
    # font=TITLE_FONT,
    # color=TITLE_COLOR,
    # size=TITLE_SIZE,
    # method='caption',
    # stroke_color=TITLE_STROKE_COLOR,
    # stroke_width=0.4,  # Width of the stroke for outline effect
    # align='center',
    # # bg_color = 'black'
    # ).set_position(TITLE_POSITION, relative=True).set_duration(duration)