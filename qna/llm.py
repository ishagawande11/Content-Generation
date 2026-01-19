# qna/llm.py

from langchain_openai import ChatOpenAI
from qna.prompt import build_prompt
from qna.retriever import retrieve_chunks

llm = ChatOpenAI(temperature=0)


def answer_question(document_id: str, question: str) -> str:
    chunks = retrieve_chunks(document_id, question)

    if not chunks:
        return "I don't know."

    context = "\n\n".join(chunks)
    prompt = build_prompt(context, question)

    response = llm.invoke(prompt)
    return response.content
