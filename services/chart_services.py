import base64
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()


def encode_image(image_bytes: bytes) -> str:
    """
    Converts raw image bytes to base64 string
    """
    return base64.b64encode(image_bytes).decode("utf-8")


def analyze_document_image(image_bytes: bytes):
    """
    Analyzes any document image (chart, report, invoice, report card, etc.)
    and returns context-aware structured JSON.
    """

    image_base64 = encode_image(image_bytes)

    prompt = """
You are an intelligent document understanding system.

Your task:
1. Identify what kind of document this image represents
   (e.g., chart, annual report, invoice, school report card, certificate, brochure, etc.)
2. Understand the visual and textual context of the document
3. Extract the most relevant information in a structured way that naturally fits this document type

Rules:
- Do NOT force a predefined schema
- Use clear, meaningful JSON keys based on the document context
- Represent tables, sections, grades, metrics, or charts naturally if present
- Do NOT invent information
- If values are estimated from visuals, explicitly mention it
- If information is unclear or missing, add a note

Return ONLY valid JSON.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        temperature=0
    )

    # Raw JSON string from model
    output = response.choices[0].message.content

    # Optional: parse to Python dict 
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return {
            "error": "Model did not return valid JSON",
            "raw_output": output
        }
