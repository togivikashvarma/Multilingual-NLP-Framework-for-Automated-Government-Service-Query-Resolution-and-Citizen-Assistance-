# Multilingual NLP Framework for Automated Government Service Query Resolution and Citizen Assistance

An educational AI assistant prototype for answering public-service questions in **English, Telugu, Hindi, Tamil and Kannada**. It combines FastAPI, Streamlit, PDF-based retrieval (RAG), and Gemini/Groq API providers.

> This is not an official government service. It does not submit applications, verify citizen identity, or access government databases. Always verify rules, fees, eligibility and deadlines on official government websites.

## 1. Features

- Five-language script-based language detection.
- Chat interface with automatic or manually selected response language.
- Gemini and Groq provider selection/fallback (`LLM_PROVIDER=auto`).
- Upload searchable PDF documents and retrieve relevant text passages.
- SQLite storage for document chunks and citizen feedback.
- FastAPI Swagger documentation and health endpoint.
- Streamlit dashboard.
- Docker Compose setup and basic language-detection tests.

## 2. Project structure

```text
multilingual-government-ai/
├── backend/
│   └── app/
│       ├── config.py
│       ├── database.py
│       ├── language.py
│       ├── llm.py
│       ├── main.py
│       ├── retrieval.py
│       └── schemas.py
├── frontend/
│   └── dashboard.py
├── data/
│   └── government_faq_sample.csv
├── storage/
├── tests/
│   └── test_language.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 3. Windows installation (PowerShell)

Open PowerShell in the project root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and add one or both API keys. Obtain keys from the providers' official developer consoles. Never commit `.env` to GitHub.

```dotenv
LLM_PROVIDER=auto
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
GEMINI_MODEL=gemini-2.5-flash
GROQ_MODEL=llama-3.3-70b-versatile
```

If PowerShell blocks activation, use:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Run the backend

From the project root, in Terminal 1:

```powershell
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Check:
- Health: http://127.0.0.1:8000/health
- API docs: http://127.0.0.1:8000/docs

Expected health response:
```json
{"status":"ok"}
```

## 5. Run the dashboard

Open Terminal 2, activate the same virtual environment, then:

```powershell
python -m streamlit run frontend/dashboard.py
```

Open http://localhost:8501.

## 6. Test PDF upload

1. Start the backend and dashboard.
2. In the dashboard sidebar, choose a text-based/searchable PDF.
3. Click **Upload and index**.
4. Ask a question that is answered by the uploaded document.
5. The assistant will retrieve matching text chunks and pass them as context to the configured model.

Scanned/image-only PDFs are not OCR-processed in this starter version. Convert them to searchable PDFs before uploading. Maximum file size: 25 MB.

## 7. API examples

Chat:
```powershell
$body = @{
  message = "How can I check my application status?"
  language = "auto"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/chat" -Method Post -ContentType "application/json" -Body $body
```

Upload:
```powershell
curl.exe -X POST "http://127.0.0.1:8000/api/v1/documents/upload" -F "file=@C:\path\to\your-document.pdf"
```

## 8. Run tests

```powershell
python -m pytest -q
```

## 9. Docker

Docker Desktop must be running:

```powershell
docker compose up --build
```

Dashboard: http://localhost:8501  
API docs: http://localhost:8000/docs

## 10. Important limitations and next development milestones

This is a runnable foundation, not a production government platform.

- Language detection currently uses Unicode script ranges; Romanized Telugu/Hindi/Tamil/Kannada may be detected as English.
- Retrieval uses a lightweight keyword-overlap method. Replace with multilingual sentence-transformer embeddings and FAISS for stronger semantic retrieval.
- PDF extraction works for selectable text; OCR, document provenance and source-page tracking are future enhancements.
- Add curated, verified official government sources and update schedules before presenting scheme-specific guidance.
- Add authentication, role-based access, encryption, rate limiting, audit logs, abuse prevention, privacy review and security testing before any public deployment.
- Never collect Aadhaar numbers, OTPs, passwords, bank PINs or unnecessary personal data.

## 11. Suggested major-project modules

1. Multilingual input and language identification.
2. Query intent classification (scheme, eligibility, documents, application status, grievance).
3. Government knowledge-base ingestion and validation.
4. Multilingual RAG retrieval and answer generation.
5. Citizen feedback and response-quality evaluation.
6. Admin analytics and monitoring.
7. Security, privacy and deployment.

## 12. Suggested evaluation

Evaluate each of the five languages with a reviewed test set. Track language-detection accuracy, retrieval Precision@K/Recall@K, answer faithfulness, answer relevance, response latency and user feedback. Have a fluent speaker review generated responses; do not rely only on automatic metrics.
