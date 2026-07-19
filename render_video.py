import os
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips
from PIL import Image

# Settings
AUDIO_PATH = "master_voiceover.mp3"
IMAGE_DIR = "assets"
OUTPUT_NAME = "Why_Developers_Need_GitHub_in_2026_full.mp4"
RESOLUTION = (854, 480)
FPS = 24

def create_video():
    # 1. Load Audio
    voiceover = AudioFileClip(AUDIO_PATH)
    total_duration = voiceover.duration
    
    # 2. Prepare Visuals
    images = sorted([os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if f.endswith('.png')])
    if not images:
        print("No images found!")
        return
        
    clips = []
    duration_per_image = total_duration / len(images)
    
    for i, img_path in enumerate(images):
        # Resize image
        with Image.open(img_path) as img:
            img = img.convert("RGB")
            img = img.resize(RESOLUTION, Image.Resampling.LANCZOS)
            img.save(f"temp_img_{i}.jpg")
        
        img_clip = ImageClip(f"temp_img_{i}.jpg").with_duration(duration_per_image)
        clips.append(img_clip)
    
    # 3. Combine Clips
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.with_audio(voiceover)
    
    # 4. Export
    final_video.write_videofile(OUTPUT_NAME, fps=FPS, codec="libx264", audio_codec="aac")
    
    # Cleanup
    for i in range(len(images)):
        if os.path.exists(f"temp_img_{i}.jpg"):
            os.remove(f"temp_img_{i}.jpg")

if __name__ == "__main__":
    create_video()
