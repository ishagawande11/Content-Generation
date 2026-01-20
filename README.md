# Content-Generation

Document Q&A using AI

Upload documents, images, or URLs and ask questions. Answers are generated strictly from the uploaded content.

Backend (port 8000):
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000

Storage:
Uses local file storage + FAISS vector index (no database required)

Key Files – Backend:

•app.py – FastAPI routes (upload, URL ingest, ask question)

•ingestion/ingest_text.py – Text chunking & embedding pipeline

•ingestion/ingest_image.py – Image OCR + analysis

•ingestion/url_ingest.py – Website ingestion

•qna/llm.py – Question answering logic (RAG)

•qna/retriever.py – FAISS similarity search

•vectorstore/faiss_db.py – FAISS index handling
