# ingestion/loader_text.py
import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException
from services.text_extractor import extract_text_from_pdf, extract_text_from_docx
from ingestion.ingest_text import ingest_text

BASE_STORAGE = "storage"
DOC_DIR = os.path.join(BASE_STORAGE, "documents")
TEXT_DIR = os.path.join(BASE_STORAGE, "texts")

os.makedirs(DOC_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)

async def ingest_document(file: UploadFile):
    document_id = str(uuid.uuid4())
    file_ext = file.filename.split(".")[-1].lower()
    doc_path = os.path.join(DOC_DIR, f"{document_id}.{file_ext}")

    with open(doc_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    extracted_text = None
    if file_ext == "pdf":
        extracted_text = extract_text_from_pdf(doc_path)
    elif file_ext == "docx":
        extracted_text = extract_text_from_docx(doc_path)
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only PDF and DOCX allowed."
        )

    if not extracted_text or not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in document"
        )

    text_path = os.path.join(TEXT_DIR, f"{document_id}.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    return ingest_text(extracted_text)
