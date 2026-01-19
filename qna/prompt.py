# qna/prompt.py

def build_prompt(context: str, question: str) -> str:
    return f"""
You are a document-based assistant.
Answer the question using ONLY the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}
"""
