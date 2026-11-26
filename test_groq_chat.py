
import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

url = "https://api.groq.com/openai/v1/chat/completions"

response = requests.post(
    url,
    headers={
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    },
    json={
        "model": "openai/gpt-oss-20b",
        "messages": [
            {
                "role": "user",
                "content": "Explain how citizens can find government services in India."
            }
        ],
        "max_completion_tokens": 300
    },
    timeout=60
)

print("Status:", response.status_code)

if response.ok:
    print("AI ANSWER:")
    print(response.json()["choices"][0]["message"]["content"])
else:
    print("ERROR:", response.text[:1500])
