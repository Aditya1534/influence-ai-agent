import os
import json
import traceback
from dotenv import load_dotenv
import requests

# Load .env file
load_dotenv()

# Get OpenRouter key
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

def load_user_profile():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "user_profile.json")
        with open(path, "r") as f:
            print("✅ Loaded user_profile.json")
            return json.load(f)
    except Exception as e:
        print("❌ Error loading profile:", e)
        return {}

def generate_post(profile):
    try:
        name = profile.get("name", "a professional")
        title = profile.get("title", "enthusiast")
        interests = ', '.join(profile.get("interests", [])) or "various topics"
        skills = ', '.join(profile.get("skills", [])) or "multiple skills"
        industry = profile.get("industry", "tech")
        if isinstance(industry, list):
            industry = ', '.join(industry)

        prompt = f"""
        Create a professional LinkedIn post for {name}, a {title} in {industry}. 
        Highlight their expertise in {skills} and interest in {interests}.
        Make it engaging and suitable for LinkedIn's professional audience.
        Include relevant hashtags and keep it under 250 words.
        """

        print("🧠 Sending prompt to OpenRouter...\n")

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openai/gpt-3.5-turbo",  # you can also try "openai/gpt-4" if allowed
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 300
        }

        res = requests.post(url, headers=headers, json=data)
        res.raise_for_status()
        output = res.json()["choices"][0]["message"]["content"]
        print("✅ Post Generated:\n")
        return output

    except Exception as e:
        print("❌ Failed to generate post:", e)
        traceback.print_exc()
        return None

if __name__ == "__main__":
    profile = load_user_profile()
    if profile:
        post = generate_post(profile)
        if post:
            print(post)
        else:
            print("⚠️ Could not generate post.")
    else:
        print("⚠️ Could not load profile.")
