# main.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from scripts.trending import get_trending_topic_from_rss as get_trending_topic
from scripts.text_to_speech import text_to_speech
from scripts.video_generator import generate_video



load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_script(topic):
    prompt = f"Write a 60-second engaging YouTube video script about the trending topic: {topic}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    topic = get_trending_topic()
    print(f"Using trending topic: {topic}")

    script = generate_script(topic)
    print("\nGenerated Script:\n")
    print(script)

    # save to file
    with open("data/script.txt", "w") as f:
        f.write(script)
    
    # convert to mp3
    text_to_speech(script)
    os.system("afplay data/voiceover.mp3")

    # Convert to audio
    text_to_speech(script)

    # Generate video with text overlay and voiceover
    generate_video(audio_path="data/voiceover.mp3", text=script)


