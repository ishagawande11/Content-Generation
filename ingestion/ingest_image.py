# ingestion/ingest_image.py

import io
from PIL import Image
import pytesseract  # OCR
from openai import OpenAI
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


client = OpenAI()

VISION_PROMPT = """
You are an expert data analyst reading business reports.

Analyze the following extracted text carefully and describe insights, trends, or key takeaways.

If it contains a chart or table:
- Identify type of chart (bar, line, pie, etc.)
- Identify axes, labels, categories
- Estimate key numerical trends
- Provide a clear, factual summary

Do NOT hallucinate numbers. If unsure, mention approximate or missing values.

Output a concise, structured explanation in plain text.
"""

def ocr_image(file_bytes: bytes) -> str:
    """Extract text from an image using OCR"""
    image = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(image)
    return text.strip()

def ingest_image_bytes(file_bytes: bytes) -> str:
    """
    Analyze an image:
    1. Extract text using OCR
    2. Send extracted text to GPT for analysis
    """
    # Step 1: OCR
    extracted_text = ocr_image(file_bytes)
    if not extracted_text:
        return "No readable text found in the image."

    # Step 2: GPT analysis
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"{VISION_PROMPT}\n\nExtracted Text:\n{extracted_text}"}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
