from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=2, max_length=4000)
    language: str = "auto"
    session_id: Optional[str] = None

class Source(BaseModel):
    title: str
    content: str

class ChatResponse(BaseModel):
    answer: str
    detected_language: str
    provider: str
    sources: List[Source] = []
    disclaimer: str = "Information is for general guidance. Verify important details on the relevant official government portal."

class DocumentInfo(BaseModel):
    filename: str
    chunks_added: int
    message: str
