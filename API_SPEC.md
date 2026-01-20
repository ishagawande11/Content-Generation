

```md
# Content Generation API – Specification

## Overview
FastAPI-based backend to ingest documents or URLs, generate embeddings,
and answer questions using Retrieval-Augmented Generation (RAG).
Also supports OCR-based image analysis.

Base URL: http://127.0.0.1:8000  
Format: JSON


## Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000


API Endpoints
1. Health Check

GET /

Checks if the backend service is running.

Response:

{
  "status": "QnA service is up and running"
}

2. Upload Document

POST /upload

Uploads and ingests a document.

Supported formats:

PDF

DOCX

Request (form-data):

file (required): Document file

Response:

{
  "document_id": "43a66203-7a3e-47a2-8a21-7b3ff2733fdb",
  "status": "ingestion_complete",
  "chunks": 5
}

3. Upload From URL

POST /upload-url

Fetches and ingests text from a public webpage.

Request (JSON):

{
  "url": "https://example.com"
}


Response:

{
  "document_id": "00fe2116-ba7f-49bd-9eb2-0e50dd89806f",
  "status": "ingestion_complete",
  "chunks": 1
}

4. Ask Question (RAG)

POST /ask

Asks a question on a previously ingested document.

Request (JSON):

{
  "document_id": "00fe2116-ba7f-49bd-9eb2-0e50dd89806f",
  "question": "What is the main topic of this document?"
}


Response:

{
  "document_id": "00fe2116-ba7f-49bd-9eb2-0e50dd89806f",
  "question": "What is the main topic of this document?",
  "answer": "The main topic of this document is the use of the domain for documentation examples without needing permission."
}


If the answer is not present in the document, the system responds with:
"I don't know."

5. Image / Chart Analysis

POST /upload-image

Uploads an image and extracts text using OCR. The extracted text is analyzed
using an LLM to generate insights. This supports charts, tables, and
text-heavy images.

Supported formats:

PNG

JPG

JPEG

Request (form-data):

file (required): Image file

Response:

{
  "text": "Extracted and analyzed content from the image."
}
