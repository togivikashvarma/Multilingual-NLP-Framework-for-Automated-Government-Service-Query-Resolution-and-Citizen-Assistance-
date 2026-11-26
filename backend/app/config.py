import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

class Settings:
    app_name = os.getenv("APP_NAME", "Multilingual Government Citizen Assistant")
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    groq_api_key = os.getenv("GROQ_API_KEY", "")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    llm_provider = os.getenv("LLM_PROVIDER", "auto").lower()
    data_dir = ROOT_DIR / "data"
    uploads_dir = ROOT_DIR / "storage" / "uploads"
    database_path = ROOT_DIR / "storage" / "citizen_assistant.db"

settings = Settings()
settings.uploads_dir.mkdir(parents=True, exist_ok=True)
settings.database_path.parent.mkdir(parents=True, exist_ok=True)
