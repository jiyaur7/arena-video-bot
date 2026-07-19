import os
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
from PIL import Image
import numpy as np

# Settings
AUDIO_PATH = "master_voiceover.mp3"
IMAGE_DIR = "assets"
OUTPUT_NAME = "Why_Developers_Need_GitHub_in_2026_Pro_full.mp4"
RESOLUTION = (854, 480)
FPS = 24

def make_zoom(t, duration, zoom_ratio=0.1):
    return 1 + (zoom_ratio * t / duration)

def create_pro_video():
    # 1. Load Audio
    voiceover = AudioFileClip(AUDIO_PATH)
    total_duration = voiceover.duration
    
    # 2. Prepare Visuals
    images = sorted([os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if f.endswith('.png')])
    if not images:
        return
        
    duration_per_image = total_duration / len(images)
    clips = []
    
    for i, img_path in enumerate(images):
        with Image.open(img_path) as img:
            img = img.convert("RGB")
            img = img.resize((int(RESOLUTION[0]*1.2), int(RESOLUTION[1]*1.2)), Image.LANCZOS)
            img.save(f"temp_pro_{i}.jpg")
        
        # Create Image Clip
        img_clip = ImageClip(f"temp_pro_{i}.jpg").with_duration(duration_per_image)
        
        # Manual Zoom using resizing effect
        def zoom(get_frame, t):
            frame = get_frame(t)
            img = Image.fromarray(frame)
            w, h = img.size
            zoom_factor = make_zoom(t, duration_per_image)
            
            # Calculate new crop
            new_w, new_h = int(RESOLUTION[0] / zoom_factor), int(RESOLUTION[1] / zoom_factor)
            left = (w - new_w) / 2
            top = (h - new_h) / 2
            
            img = img.crop((left, top, left + new_w, top + new_h))
            img = img.resize(RESOLUTION, Image.LANCZOS)
            return np.array(img)
            
        img_clip = img_clip.transform(zoom)
        clips.append(img_clip)
    
    # 3. Combine Clips with transitions
    # Using simple concatenation first, then we'll add more if needed
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.with_audio(voiceover)
    
    # 4. Export
    final_video.write_videofile(OUTPUT_NAME, fps=FPS, codec="libx264", audio_codec="aac")
    
    # Cleanup
    for i in range(len(images)):
        if os.path.exists(f"temp_pro_{i}.jpg"):
            os.remove(f"temp_pro_{i}.jpg")

if __name__ == "__main__":
    create_pro_video()
