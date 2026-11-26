import re
from collections import Counter
from backend.app.database import get_chunks

def tokens(text):
    return set(re.findall(r"[\w\u0900-\u0D7F]+", text.lower()))

def retrieve(query, top_k=4):
    query_terms = tokens(query)
    candidates = get_chunks()
    scored = []
    for item in candidates:
        terms = tokens(item["chunk_text"])
        score = len(query_terms & terms) / max(1, len(query_terms))
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        {"title": item["filename"], "content": item["chunk_text"]}
        for score, item in scored[:top_k]
    ]
