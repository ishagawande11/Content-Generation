# routes/chart.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from services.chart_services import analyze_document_image

router = APIRouter(
    prefix="/chart",
    tags=["Document Analysis"]
)


@router.post("/analyze")
async def analyze_chart(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are supported"
        )

    image_bytes = await file.read()

    try:
        # ✅ THIS ALREADY RETURNS A DICT
        analysis = analyze_document_image(image_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document analysis failed: {str(e)}"
        )

    return {
        "status": "success",
        "analysis": analysis,
        "note": "Schema is inferred dynamically based on document context"
    }
