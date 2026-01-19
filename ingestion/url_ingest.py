# ingestion/url_ingest.py
from fastapi import HTTPException
from ingestion.ingest_text import ingest_text
from services.url_loader import fetch_website_pages

def ingest_url(url: str, max_pages: int = 5):
    """
    Fetch text from a URL and ingest it using your text ingestion pipeline.
    """
    try:
        pages = fetch_website_pages(url, max_pages=max_pages)
        if not pages:
            raise ValueError("No content could be fetched from URL")

        full_text = "\n\n".join(pages)
        return ingest_text(full_text)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to ingest URL: {str(e)}"
        )
