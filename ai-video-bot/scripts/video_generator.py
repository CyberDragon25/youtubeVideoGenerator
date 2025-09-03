# scripts/video_generator.py

from scripts.image_generator import generate_image_from_prompt

from moviepy.editor import *
from gtts import gTTS
import os
os.environ["IMAGEMAGICK_BINARY"] = "/usr/local/bin/convert"  # or whatever `which convert` gives

import re
import uuid

def split_script_into_sentences(script):
    # Basic split on punctuation
    return re.split(r'(?<=[.!?])\s+', script.strip())

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

def generate_video_from_script(script, output_path="data/final_video.mp4"):
    sentences = split_script_into_sentences(script)
    clips = []

    os.makedirs("data/scenes", exist_ok=True)

    for i, sentence in enumerate(sentences):
        if len(sentence.strip()) == 0:
            continue

        print(f"[🎬] Generating scene {i+1}: \"{sentence}\"")

        # 1. Generate audio
        audio_path = f"data/scenes/scene_{i}.mp3"
        text_to_speech(sentence, audio_path)
        audio = AudioFileClip(audio_path)

        # 2. Generate image with DALLE
        image_path = generate_image_from_prompt(sentence, i)
        img_clip = ImageClip(image_path).set_duration(audio.duration).resize((1280, 720))


        # 3. Text overlay
        txt = TextClip(sentence, fontsize=40, color='white', size=(1200, None), method='caption')
        txt = txt.set_position("center").set_duration(audio.duration)

        # 4. Combine
        scene = CompositeVideoClip([img_clip, txt]).set_audio(audio)
        clips.append(scene)

    final = concatenate_videoclips(clips, method="compose")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final.write_videofile(output_path, fps=24)
    print(f"[✅] Final video saved to {output_path}")
