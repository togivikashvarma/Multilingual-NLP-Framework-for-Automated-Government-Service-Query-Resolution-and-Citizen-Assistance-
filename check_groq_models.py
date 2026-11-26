
import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

key = os.getenv("GROQ_API_KEY")

if not key:
    print("GROQ_API_KEY is missing")
    raise SystemExit(1)

response = requests.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {key}"},
    timeout=30
)

print("HTTP:", response.status_code)

if response.ok:
    for model in response.json().get("data", []):
        print(model["id"])
else:
    print(response.text[:1500])
