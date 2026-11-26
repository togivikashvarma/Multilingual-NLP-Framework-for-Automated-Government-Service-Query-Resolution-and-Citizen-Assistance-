from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from io import BytesIO

from backend.app.config import settings
from backend.app.database import initialize, add_chunks, list_documents, save_feedback
from backend.app.schemas import ChatRequest, ChatResponse, DocumentInfo
from backend.app.language import detect_language
from backend.app.retrieval import retrieve
from backend.app.llm import generate_answer

app = FastAPI(
    title=settings.app_name,
    description="Multilingual citizen assistance using retrieval-augmented generation.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:8501"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

@app.on_event("startup")
def startup():
    initialize()

@app.get("/")
def root():
    return {"message": settings.app_name, "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    language = detect_language(request.message) if request.language == "auto" else request.language
    if language not in {"en", "te", "hi", "ta", "kn"}:
        language = detect_language(request.message)
    sources = retrieve(request.message)
    answer, provider = generate_answer(request.message, sources, language)
    return ChatResponse(
        answer=answer, detected_language=language,
        provider=provider, sources=sources
    )

@app.post("/api/v1/documents/upload", response_model=DocumentInfo)
async def upload_document(file: UploadFile = File(...)):
    filename = Path(file.filename or "document").name
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    raw = await file.read()
    if len(raw) > 25 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Maximum upload size is 25 MB.")
    try:
        reader = PdfReader(BytesIO(raw))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {exc}")
    if not text.strip():
        raise HTTPException(status_code=400, detail="No selectable text found. Scanned PDFs need OCR.")
    chunks = [text[i:i+1000] for i in range(0, len(text), 850)]
    add_chunks(filename, chunks)
    return DocumentInfo(filename=filename, chunks_added=len(chunks),
                        message="PDF processed and indexed successfully.")

@app.get("/api/v1/documents")
def documents():
    return {"documents": list_documents()}

@app.post("/api/v1/feedback")
def feedback(payload: dict):
    rating = int(payload.get("rating", 0))
    if rating not in range(1, 6):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")
    save_feedback(payload.get("session_id"), payload.get("question", ""),
                  rating, payload.get("comment", ""))
    return {"status": "saved"}
