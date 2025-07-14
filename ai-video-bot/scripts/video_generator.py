# scripts/video_generator.py

import moviepy.editor as mp
import os

def generate_video(audio_path="data/voiceover.mp3", text="", output_path="data/video.mp4"):
    # Load audio
    audio = mp.AudioFileClip(audio_path)

    # Create a blank background clip (black, white, or custom image)
    video = mp.ColorClip(size=(1280, 720), color=(10, 10, 10), duration=audio.duration)

    # Set audio
    video = video.set_audio(audio)

    # Create text overlay
    txt_clip = mp.TextClip(text, fontsize=40, color='white', font='Arial-Bold', size=(1200, None), method='caption')
    txt_clip = txt_clip.set_position('center').set_duration(audio.duration)

    # Composite text on video
    final = mp.CompositeVideoClip([video, txt_clip])

    # Export video
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final.write_videofile(output_path, fps=24)

    print(f"[✅] Video saved to {output_path}")
