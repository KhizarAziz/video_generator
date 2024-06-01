import os
from moviepy.editor import (
    ImageClip, AudioFileClip, TextClip, CompositeVideoClip,
    vfx, concatenate_videoclips
)
from pydub import AudioSegment
from textwrap import wrap
from .video_configs import (
    FPS, BRIGHTNESS_FACTOR, SPEED_FACTOR,
    TITLE_FONTSIZE, TITLE_FONTSIZE_SHADOW, TITLE_FONT, TITLE_COLOR,
    TITLE_SHADOW_COLOR, TITLE_POSITION, SUBTITLE_FONTSIZE, SUBTITLE_FONTSIZE_SHADOW,
    SUBTITLE_FONT, SUBTITLE_COLOR, SUBTITLE_SHADOW_COLOR, SUBTITLE_POSITION,
    MAX_CHARS_PER_LINE, CHUNK_SIZE
)


def split_text_into_chunks(text: str, chunk_size: int = CHUNK_SIZE) -> list:
    """
    Split text into chunks of a specified size.

    Args:
        text (str): Text to split.
        chunk_size (int, optional): Number of words per chunk. Defaults to 7.

    Returns:
        list: List of text chunks.
    """
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def create_subtitle_clips(text: str, title: str, duration: float, chunk_size: int = CHUNK_SIZE) -> list:
    """
    Create subtitle clips from text, split into chunks, ensuring each chunk fits within the frame.

    Args:
        text (str): Text to display as subtitles.
        duration (float): Duration of the audio.
        chunk_size (int, optional): Number of words per subtitle chunk. Defaults to 7.

    Returns:
        list: List of subtitle clips.
    """
    chunks = split_text_into_chunks(text, chunk_size)
    chunk_duration = duration / len(chunks)
    subtitle_clips = []

    # Create the title clip with bold font and larger size with shadow
    title_shadow = TextClip(
        title, fontsize=TITLE_FONTSIZE_SHADOW, font=TITLE_FONT, color=TITLE_SHADOW_COLOR,
        size=(1080, None), method='caption'
    ).set_position(TITLE_POSITION, relative=True).set_duration(duration).set_opacity(0.6)

    title_clip = TextClip(
        title, fontsize=TITLE_FONTSIZE, font=TITLE_FONT, color=TITLE_COLOR,
        size=(1080, None), method='caption'
    ).set_position(TITLE_POSITION, relative=True).set_duration(duration)

    subtitle_clips.append(title_shadow)
    subtitle_clips.append(title_clip)

    for i, chunk in enumerate(chunks):
        wrapped_text = "\n".join(wrap(chunk, MAX_CHARS_PER_LINE))

        subtitle_shadow = TextClip(
            wrapped_text, fontsize=SUBTITLE_FONTSIZE_SHADOW, font=SUBTITLE_FONT, color=SUBTITLE_SHADOW_COLOR,
            size=(1080, None), method='caption'
        ).set_position(SUBTITLE_POSITION).set_duration(chunk_duration).set_start(i * chunk_duration)

        subtitle_clip = TextClip(
            wrapped_text, fontsize=SUBTITLE_FONTSIZE, font=SUBTITLE_FONT, color=SUBTITLE_COLOR,
            size=(1080, None), method='caption'
        ).set_position(SUBTITLE_POSITION).set_duration(chunk_duration).set_start(i * chunk_duration)

        subtitle_clips.append(subtitle_shadow)
        subtitle_clips.append(subtitle_clip)

    return subtitle_clips

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

    return CompositeVideoClip([video_clip, *subtitle_clips])




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

def save_video(clip: CompositeVideoClip, output_path: str, fps: int = FPS):
    """
    Save the video clip to a file.

    Args:
        clip (CompositeVideoClip): Video clip to save.
        output_path (str): Path to save the final video.
        fps (int, optional): Frames per second for the video. Defaults to 12.
    """
    clip.write_videofile(output_path, fps=fps, codec="libx264", audio_codec="aac")
    print(f"Video saved to {output_path}")

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