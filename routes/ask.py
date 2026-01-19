from fastapi import FastAPI
from pydantic import BaseModel
from qna.llm import answer_question

app = FastAPI()

class AskRequest(BaseModel):
    document_id: str
    question: str

@app.post("/ask")
def ask(req: AskRequest):
    result = answer_question(
        question=req.question,
        document_id=req.document_id
    )

    return {
        "document_id": req.document_id,
        "question": req.question,
        **result
    }
