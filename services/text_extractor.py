# services/text_extractor.py
from PyPDF2 import PdfReader
import docx
from fastapi import HTTPException
import re

def normalize_text(text: str) -> str:
    text = text.replace('\r', '')
    lines = [line.strip() for line in text.splitlines()]

    paragraphs = []
    current_para = ""

    for line in lines:
        if not line:
            if current_para:
                paragraphs.append(current_para.strip())
                current_para = ""
            continue

        # bullet points / numbered lists
        if re.match(r'^(\•|\-|\*|\d+\.)', line):
            if current_para:
                paragraphs.append(current_para.strip())
            paragraphs.append(line)
            current_para = ""
        else:
            current_para += " " + line if current_para else line

    if current_para:
        paragraphs.append(current_para.strip())

    return "\n\n".join(paragraphs)

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF reading error: {str(e)}")

    return normalize_text(text)

def extract_text_from_docx(file_path: str) -> str:
    text = ""
    doc = docx.Document(file_path)
    raw_text = "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return normalize_text(raw_text)
