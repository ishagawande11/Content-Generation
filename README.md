# Content-Generation

Upload documents, images, or URLs and ask questions. Answers are generated from the uploaded content using a retrieval-based AI pipeline.

## Backend (port 8000)
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## Storage
Local file storage for uploaded documents and extracted text  
FAISS vector index for semantic search  
No database required  

## Key Files – Backend

### app.py
FastAPI routes for document upload, URL ingestion, image ingestion, and question answering  

### ingestion/ingest_text.py
Text chunking, embedding generation, and FAISS indexing pipeline  

### ingestion/ingest_image.py
Image OCR and AI-based content analysis  

### ingestion/url_ingest.py
Website content ingestion and preprocessing  

### qna/llm.py
Retrieval-augmented question answering logic using LangChain  

### qna/retriever.py
FAISS-based similarity search over document chunks  

### vectorstore/faiss_db.py
FAISS index creation, saving, and loading utilities
