# ingestion/ingest_text.py
import os
import uuid
from ingestion.chunker import split_text
from ingestion.embedder import embed_chunks
from vectorstore.faiss_db import (
    create_faiss_index,
    save_index,
    save_chunks
)

BASE_STORAGE = "storage"
VECTOR_DIR = os.path.join(BASE_STORAGE, "vectors")
os.makedirs(VECTOR_DIR, exist_ok=True)

def ingest_text(text: str):
    document_id = str(uuid.uuid4())
    
    chunks = split_text(text)
    embeddings = embed_chunks(chunks)
    index = create_faiss_index(embeddings)
    
    index_path = os.path.join(VECTOR_DIR, f"{document_id}.faiss")
    chunks_path = os.path.join(VECTOR_DIR, f"{document_id}.npy")
    
    save_index(index, index_path)
    save_chunks(chunks, chunks_path)
    
    return {
        "document_id": document_id,
        "status": "ingestion_complete",
        "chunks": len(chunks)
    }
