import requests
from backend.app.config import settings
from backend.app.language import language_name

def _prompt(question, context, language):
    context_text = "\n\n".join(
        f"[Source: {s['title']}]\n{s['content']}" for s in context
    ) or "No uploaded document passages were retrieved."
    return f"""
You are a careful public-service information assistant.
Reply in {language_name(language)}.
Question: {question}

Retrieved information:
{context_text}

Rules:
- Give clear, practical steps in simple language.
- Use only supported facts from the retrieved information when describing specific rules.
- If the context does not contain the answer, say that you cannot verify it and direct the citizen to the relevant official government website or office.
- Never invent eligibility rules, fees, deadlines, phone numbers, URLs, or required documents.
- Do not claim to submit applications or access government databases.
- Include a short safety reminder not to share Aadhaar number, OTP, passwords, bank PINs, or other sensitive credentials in chat.
"""

def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent"
    response = requests.post(
        url, params={"key": settings.gemini_api_key},
        json={"contents": [{"parts": [{"text": prompt}]}],
              "generationConfig": {"temperature": 0.2}},
        timeout=45
    )
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def ask_groq(prompt):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {settings.groq_api_key}"},
        json={
            "model": settings.groq_model,
            "messages": [
                {"role": "system", "content": "You are a careful multilingual government service assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        },
        timeout=45
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def generate_answer(question, context, language):
    prompt = _prompt(question, context, language)
    providers = []
    if settings.llm_provider == "gemini":
        providers = [("gemini", ask_gemini, settings.gemini_api_key)]
    elif settings.llm_provider == "groq":
        providers = [("groq", ask_groq, settings.groq_api_key)]
    else:
        providers = [
            ("gemini", ask_gemini, settings.gemini_api_key),
            ("groq", ask_groq, settings.groq_api_key)
        ]
    errors = []
    for name, function, key in providers:
        if not key:
            errors.append(f"{name}: API key not configured")
            continue
        try:
            return function(prompt), name
        except Exception as exc:
            errors.append(f"{name}: {str(exc)[:250]}")
    fallback = (
        "I can help with general guidance, but the AI service is not configured or is temporarily unavailable. "
        "Please add a valid Gemini or Groq API key in the .env file and restart the backend. "
        "For official information, use the relevant government portal. Do not share OTPs or passwords."
    )
    return fallback + "\n\nProvider status: " + "; ".join(errors), "local-fallback"
