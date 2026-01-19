from services.retriever import retrieve_chunks
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)


def answer_question(document_id: str, question: str):
    chunks = retrieve_chunks(document_id, question)

    if not chunks:
        return "I don't know. The document does not contain this information."

    context = "\n\n".join(chunks)

    prompt = f"""
You are a document-based assistant.
Answer the question using ONLY the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)
    return response.content
