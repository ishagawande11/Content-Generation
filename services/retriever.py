import os
import numpy as np
from vectorstore.faiss_db import load_index, load_chunks
from ingestion.embedder import get_embedding_model

BASE_STORAGE = "storage"
VECTOR_DIR = os.path.join(BASE_STORAGE, "vectors")


def retrieve_chunks(document_id: str, query: str, top_k: int = 4):
    index_path = os.path.join(VECTOR_DIR, f"{document_id}.faiss")
    chunks_path = os.path.join(VECTOR_DIR, f"{document_id}.npy")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        raise ValueError("Document not found")

    index = load_index(index_path)
    chunks = load_chunks(chunks_path)

    model = get_embedding_model()
    query_embedding = model.encode([query], convert_to_numpy=True)

    distances, indices = index.search(query_embedding, top_k)

    retrieved = []
    for idx in indices[0]:
        if idx < len(chunks):
            retrieved.append(chunks[idx])

    return retrieved