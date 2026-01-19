# ingestion/embedder.py
from sentence_transformers import SentenceTransformer

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        print("Loading embedding model...")
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model

def embed_chunks(chunks: list[str]):
    model = get_embedding_model()
    return model.encode(chunks, convert_to_numpy=True)
