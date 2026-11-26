from backend.app.language import detect_language

def test_english():
    assert detect_language("How can I apply?") == "en"

def test_telugu():
    assert detect_language("ఆధార్ కార్డు ఎలా అప్లై చేయాలి?") == "te"

def test_hindi():
    assert detect_language("आवेदन कैसे करें?") == "hi"

def test_tamil():
    assert detect_language("எப்படி விண்ணப்பிப்பது?") == "ta"

def test_kannada():
    assert detect_language("ಅರ್ಜಿ ಹೇಗೆ ಸಲ್ಲಿಸಬೇಕು?") == "kn"
