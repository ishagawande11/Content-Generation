import faiss
import numpy as np
import os

def create_faiss_index(embeddings: np.ndarray):
    if embeddings.size == 0:
        raise ValueError("No embeddings to index")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

def save_index(index, index_path: str):
    faiss.write_index(index, index_path)

def load_index(index_path: str):
    return faiss.read_index(index_path)

def save_chunks(chunks: list[str], path: str):
    np.save(path, np.array(chunks, dtype=object))

def load_chunks(path: str):
    return np.load(path, allow_pickle=True)
