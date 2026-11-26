
import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

groq_key = os.getenv("GROQ_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

print("\n--- GROQ TEST ---")

if groq_key:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": "Reply with Hello"}
            ],
            "temperature": 0.2
        },
        timeout=30
    )

    print("Status:", response.status_code)
    print("Response:", response.text[:1500])
else:
    print("Groq key missing")

print("\n--- GEMINI TEST ---")

if gemini_key:
    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-3.8-flash:generateContent"
    )

    response = requests.post(
        url,
        params={"key": gemini_key},
        json={
            "contents": [{
                "parts": [{"text": "Reply with Hello"}]
            }]
        },
        timeout=30
    )

    print("Status:", response.status_code)
    print("Response:", response.text[:1500])
else:
    print("Gemini key missing")
