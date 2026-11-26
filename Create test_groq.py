
import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")
model = "openai/gpt-oss-20b"

if not api_key:
    raise ValueError("GROQ_API_KEY is missing")

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": "Explain how citizens can access government services in simple English."
            }
        ],
        "temperature": 0.2,
        "max_tokens": 300
    },
    timeout=60
)

print("HTTP Status:", response.status_code)

if response.ok:
    data = response.json()
    print("Model:", data.get("model"))
    print("AI Response:", data["choices"][0]["message"]["content"])
else:
    print("Error:", response.text[:1500])
