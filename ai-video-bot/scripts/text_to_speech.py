# scripts/text_to_speech.py

from gtts import gTTS
import os

def text_to_speech(text, filename="data/voiceover.mp3"):
    tts = gTTS(text=text, lang='en')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    tts.save(filename)
    print(f"[✅] Audio saved to {filename}")
