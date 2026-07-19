import os
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips, CompositeAudioClip
import numpy as np
from PIL import Image

# Settings
AUDIO_PATH = "master_voiceover.mp3"
IMAGE_DIR = "assets"
OUTPUT_NAME = "Why_Developers_Need_GitHub_in_2026_Smooth_full.mp4"
RESOLUTION = (854, 480)
FPS = 30  # Higher FPS for smoothness

def create_smooth_video():
    # 1. Load Voiceover
    voiceover = AudioFileClip(AUDIO_PATH)
    total_duration = voiceover.duration
    
    # 2. Prepare Visuals
    images = sorted([os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if f.endswith('.png')])
    if not images:
        return
        
    duration_per_image = total_duration / len(images)
    clips = []
    
    for i, img_path in enumerate(images):
        # Load and pre-resize to a larger size to avoid pixelation during zoom
        with Image.open(img_path) as img:
            img = img.convert("RGB")
            # Create a 2x larger source for smooth zooming
            large_res = (RESOLUTION[0] * 2, RESOLUTION[1] * 2)
            img = img.resize(large_res, Image.Resampling.LANCZOS)
            img.save(f"temp_smooth_{i}.jpg", quality=95)
        
        # Create Clip
        img_clip = ImageClip(f"temp_smooth_{i}.jpg").with_duration(duration_per_image)
        
        # Smooth Zoom Logic (Sub-pixel calculation)
        def smooth_zoom(get_frame, t):
            frame = get_frame(t)
            img = Image.fromarray(frame)
            w, h = img.size
            
            # Very slow, subtle zoom (1.0 to 1.05 over 6 seconds)
            zoom_factor = 1 + (0.05 * t / duration_per_image)
            
            new_w, new_h = int(w / zoom_factor), int(h / zoom_factor)
            left = (w - new_w) / 2
            top = (h - new_h) / 2
            
            # Crop and resize back with high-quality filter
            img = img.crop((left, top, left + new_w, top + new_h))
            img = img.resize(RESOLUTION, Image.Resampling.BICUBIC)
            return np.array(img)
            
        img_clip = img_clip.transform(smooth_zoom)
        clips.append(img_clip)
    
    # 3. Combine Clips
    final_video = concatenate_videoclips(clips, method="compose")
    
    # 4. Audio Mixing (Voiceover only for now, can add music later)
    final_video = final_video.with_audio(voiceover)
    
    # 5. Export with High Bitrate
    final_video.write_videofile(
        OUTPUT_NAME, 
        fps=FPS, 
        codec="libx264", 
        audio_codec="aac", 
        bitrate="3000k",
        threads=4
    )
    
    # Cleanup
    for i in range(len(images)):
        if os.path.exists(f"temp_smooth_{i}.jpg"):
            os.remove(f"temp_smooth_{i}.jpg")

if __name__ == "__main__":
    create_smooth_video()
