import sqlite3
from backend.app.config import settings

def connect():
    conn = sqlite3.connect(settings.database_path)
    conn.row_factory = sqlite3.Row
    return conn

def initialize():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS document_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                chunk_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                question TEXT,
                rating INTEGER,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

def add_chunks(filename, chunks):
    with connect() as conn:
        conn.executemany(
            "INSERT INTO document_chunks(filename, chunk_text) VALUES (?, ?)",
            [(filename, chunk) for chunk in chunks]
        )

def get_chunks(limit=500):
    with connect() as conn:
        rows = conn.execute(
            "SELECT filename, chunk_text FROM document_chunks ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [dict(row) for row in rows]

def list_documents():
    with connect() as conn:
        rows = conn.execute("""
            SELECT filename, COUNT(*) AS chunks,
                   MAX(created_at) AS uploaded_at
            FROM document_chunks GROUP BY filename ORDER BY uploaded_at DESC
        """).fetchall()
    return [dict(row) for row in rows]

def save_feedback(session_id, question, rating, comment):
    with connect() as conn:
        conn.execute(
            "INSERT INTO feedback(session_id, question, rating, comment) VALUES (?, ?, ?, ?)",
            (session_id, question, rating, comment)
        )
