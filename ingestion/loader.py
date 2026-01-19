import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException

from services.text_extractor import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from ingestion.ingest_text import ingest_text
from ingestion.ingest_image import ingest_image_bytes  # ✅ use bytes-based function

BASE_STORAGE = "storage"

DOC_DIR = os.path.join(BASE_STORAGE, "documents")
TEXT_DIR = os.path.join(BASE_STORAGE, "texts")

os.makedirs(DOC_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)


async def ingest_document(file: UploadFile):
    document_id = str(uuid.uuid4())
    file_ext = file.filename.split(".")[-1].lower()

    # Save the uploaded file to disk (for PDFs/DOCX or backup)
    doc_path = os.path.join(DOC_DIR, f"{document_id}.{file_ext}")
    with open(doc_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    extracted_text = None

    # -------------------------------
    # IMAGE HANDLING
    # -------------------------------
    if file_ext in ["png", "jpg", "jpeg"]:
        # Read file bytes directly from UploadFile
        file.file.seek(0)  # make sure pointer is at start
        file_bytes = await file.read()
        extracted_text = ingest_image_bytes(file_bytes)  

    # -------------------------------
    # PDF HANDLING
    # -------------------------------
    elif file_ext == "pdf":
        extracted_text = extract_text_from_pdf(doc_path)

    # -------------------------------
    # DOCX HANDLING
    # -------------------------------
    elif file_ext == "docx":
        extracted_text = extract_text_from_docx(doc_path)

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only PDF, DOCX, PNG, JPG, JPEG allowed."
        )

    # -------------------------------
    # CHECK IF TEXT WAS EXTRACTED
    # -------------------------------
    if not extracted_text or not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in document"
        )

    # -------------------------------
    # SAVE EXTRACTED TEXT
    # -------------------------------
    text_path = os.path.join(TEXT_DIR, f"{document_id}.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    # -------------------------------
    # PROCESS TEXT WITH ingest_text
    # -------------------------------
    return ingest_text(extracted_text)
