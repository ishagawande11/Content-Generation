# app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from ingestion.loader_text import ingest_document
from ingestion.url_ingest import ingest_url
from pydantic import BaseModel
from ingestion.ingest_image import ingest_image_bytes
from qna.llm import answer_question
# Add import for answer_question; adjust the module path as needed (e.g., from qna import answer_question)
# from qna import answer_question

app = FastAPI()

@app.get("/")
def health():
    return {"status": "QnA service is up and running"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        return await ingest_document(file)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class URLRequest(BaseModel):
    url: str

@app.post("/upload-url")
async def upload_from_url(request: URLRequest):
    return ingest_url(request.url)

# Define AskRequest model
class AskRequest(BaseModel):
    document_id: str
    question: str

@app.post("/ask")
def ask_question(request: AskRequest):
    try:
        answer = answer_question(
            document_id=request.document_id,
            question=request.question
        )

        return {
            "document_id": request.document_id,
            "question": request.question,
            "answer": answer
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Change route to avoid conflict with the document upload
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    file_bytes = await file.read()
    text = ingest_image_bytes(file_bytes)
    return {"text": text}