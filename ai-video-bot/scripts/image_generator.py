# scripts/image_generator.py

import os
from openai import OpenAI
from dotenv import load_dotenv
import uuid

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_valid_image_size(requested="1280x720"):
    if requested == "1280x720":
        return "1792x1024"
    return "1024x1024"  # fallback

def generate_image_from_prompt(prompt, index=0):
    print(f"[🖼] Generating image for: \"{prompt}\"")

    # 🔐 Safety check for short, vague, or placeholder prompts
    if not prompt or len(prompt.strip()) < 10 or any(
        placeholder in prompt for placeholder in ["[", "]", "Dr.", "Expert", "Guest"]
    ):
        print(f"[⚠️] Skipping invalid or unsafe prompt: {prompt}")
        return "assets/default_placeholder.jpg"  # Make sure this placeholder image exists

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=get_valid_image_size("1280x720"),
            quality="standard",
            n=1
        )
        image_url = response.data[0].url

        # Save image
        import requests
        image_data = requests.get(image_url).content
        os.makedirs("data/images", exist_ok=True)
        filename = f"data/images/image_{index}.png"
        with open(filename, "wb") as f:
            f.write(image_data)

        return filename

    except Exception as e:
        print(f"[❌] Error generating image for prompt '{prompt}': {e}")
        return "assets/default_placeholder.jpg"  # Graceful fallback
