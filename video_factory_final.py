import os
import numpy as np
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont

# Settings
AUDIO_PATH = "master_voiceover.mp3"
IMAGE_DIR = "assets"
OUTPUT_NAME = "Final_Professional_Video_Fixed_full.mp4"
RESOLUTION = (854, 480)
FPS = 30

def apply_pro_motion(t, duration, img, motion_type):
    w, h = img.size
    if motion_type == "zoom_in":
        zoom = 1 + (0.1 * t / duration)
    elif motion_type == "zoom_out":
        zoom = 1.1 - (0.1 * t / duration)
    elif motion_type == "pan_right":
        zoom = 1.1
        offset = (w * 0.1) * (t / duration)
        img = img.crop((offset, 0, offset + w/1.1, h/1.1))
    else:
        zoom = 1.05
        
    new_w, new_h = int(RESOLUTION[0] * zoom), int(RESOLUTION[1] * zoom)
    img_res = img.resize((new_w, new_h), Image.Resampling.BICUBIC)
    
    # Center Crop to Resolution
    left = (new_w - RESOLUTION[0]) / 2
    top = (new_h - RESOLUTION[1]) / 2
    return np.array(img_res.crop((left, top, left + RESOLUTION[0], top + RESOLUTION[1])))

def create_final():
    voiceover = AudioFileClip(AUDIO_PATH)
    total_dur = voiceover.duration
    
    images = sorted([os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if f.endswith('.png')])
    dur_per_img = total_dur / len(images)
    
    motions = ["zoom_in", "pan_right", "zoom_out", "zoom_in", "pan_right", "zoom_out"]
    
    clips = []
    for i, img_path in enumerate(images):
        raw_img = Image.open(img_path).convert("RGB")
        raw_img = raw_img.resize((RESOLUTION[0]*2, RESOLUTION[1]*2), Image.Resampling.LANCZOS)
        
        m_type = motions[i % len(motions)]
        
        # Create clip with a transform function
        clip = ImageClip(np.array(raw_img.resize(RESOLUTION))).with_duration(dur_per_img)
        clip = clip.transform(lambda get_frame, t: apply_pro_motion(t, dur_per_img, raw_img, m_type))
        clips.append(clip)
        
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.with_audio(voiceover)
    final_video.write_videofile(OUTPUT_NAME, fps=FPS, codec="libx264", audio_codec="aac", bitrate="3000k")

if __name__ == "__main__":
    create_final()
