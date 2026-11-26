import re

LANGUAGE_NAMES = {
    "en": "English", "te": "Telugu", "hi": "Hindi", "ta": "Tamil", "kn": "Kannada"
}
SCRIPT_PATTERNS = [
    ("te", re.compile(r"[\u0C00-\u0C7F]")),
    ("hi", re.compile(r"[\u0900-\u097F]")),
    ("ta", re.compile(r"[\u0B80-\u0BFF]")),
    ("kn", re.compile(r"[\u0C80-\u0CFF]")),
]

def detect_language(text: str) -> str:
    for code, pattern in SCRIPT_PATTERNS:
        if pattern.search(text):
            return code
    return "en"

def language_name(code: str) -> str:
    return LANGUAGE_NAMES.get(code, "English")
