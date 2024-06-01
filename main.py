import os
from utils import find_latest_json_file, load_json_data, find_latest_date
from video_generation.video_generator import create_video_clip, combine_clips,postprocess_clip, save_video


# this was the code that i used when i originally built it... mainly using a json which continas th below sample
# from configs import ASSETS_DIR
# latest_file = find_latest_json_file(ASSETS_DIR)
# if not latest_file:
#     print("No JSON files found in the directory.")
#     exit()
# data = load_json_data(latest_file)


sample_json = {
    "30-05-2024": {
        "HEADLINES & LAUNCHES": [
            {
                "title": "MISTRAL'S NEW AI NON-PRODUCTION LICENSE",
                "news": "Mistral is working to find a balance between openness and business success. It has a new license aimed at striking that balance. It will continue releasing other projects under Apache 2.0 as well as the new MNPL license.",
                "keywords": "Mistral, Apache 2.0, MNPL license",
                "frame": "Path_to_project_root/VAI/assets/frames_05-2024/2024-05-30-0.png",
                "audio": "Path_to_project_root/VAI/assets/audio_05-2024/2024-05-30-0.mp3"
            },
            {
                "title": "SONIC: A LOW-LATENCY VOICE MODEL FOR LIFELIKE SPEECH",
                "news": "A new model from the creators of SSMs, Mamba, and sub quadratic Transformer variants. Importantly, their new company Cartesia has trained a lightning-fast, realistic voice generation model. This points to their desire to move into the assistants' space.",
                "keywords": "SSMs, Mamba, Cartesia",
                "frame": "Path_to_project_root/VAI/assets/frames_05-2024/2024-05-30-1.png",
                "audio": "Path_to_project_root/VAI/assets/audio_05-2024/2024-05-30-1.mp3"
            },
            {
                "title": "VOX MEDIA AND THE ATLANTIC SIGN CONTENT DEALS WITH OPENAI (1 MINUTE READ)",
                "news": "OpenAI has signed licensing deals with The Atlantic and Vox Media, allowing their content to train its AI models and be shared in ChatGPT with proper attribution.",
                "keywords": "OpenAI, The Atlantic, Vox Media",
                "frame": "Path_to_project_root/VAI/assets/frames_05-2024/2024-05-30-2.png",
                "audio": "Path_to_project_root/VAI/assets/audio_05-2024/2024-05-30-2.mp3"
            }
        ],
        "RESEARCH & INNOVATION": [
            {
                "title": "MISTRAL'S CODE MODEL",
                "news": "Mistral released a 22B code model with 32k context. It is a powerful and fast model with broad performance across many programming languages. It has open weights and is available via Mistral's platform."
            },
            {
                "title": "PRISM: SMALL MOLECULE FOUNDATION MODEL",
                "news": "PRISM is a foundation model trained on 1.2 billion small molecule mass spectra to enhance mass spectrometry analysis in drug discovery. It uses self-supervised learning to predict molecular properties from complex mixtures without prior annotations, significantly advancing the field of metabolomics. The model improves the identification and understanding of largely unknown natural molecules, accelerating the discovery of new therapeutics by leveraging massive, previously untapped spectral data."
            },
            {
                "title": "DIFFUSION MODELS FOR INVERSE PROBLEMS",
                "news": "DMPlug is a novel plug-in method that uses pretrained diffusion models to solve inverse problems. Unlike existing interleaving methods, DMPlug views the reverse diffusion process as a function, addressing both manifold feasibility and measurement feasibility effectively."
            }
        ],
        "ENGINEERING & RESOURCES": [
            {
                "title": "ENHANCED SUPER-RESOLUTION EFFICIENCY",
                "news": "PatchScaler is a diffusion-based method for single image super-resolution that significantly enhances inference efficiency."
            },
            {
                "title": "3D UNDERSTANDING WITH ENHANCED SEGMENTATION",
                "news": "Reason3D is a novel multimodal large language model designed for comprehensive 3D environment understanding."
            }
        ]
    }
}

latest_date = find_latest_date(sample_json)

headlines_launches = sample_json[latest_date]["HEADLINES & LAUNCHES"]


all_clips = [create_video_clip(item) for item in headlines_launches]

combined_clip = combine_clips(all_clips)
postprocessed_clip = postprocess_clip(combined_clip)



ASSETS_DIR = "Path_to_assets_folder" # could be any dir
OUTPUT_VIDEO_FILENAME = latest_date + "_video.mp4"
output_path = os.path.join(ASSETS_DIR, OUTPUT_VIDEO_FILENAME)
save_video(postprocessed_clip, output_path)
