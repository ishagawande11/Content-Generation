# services/url_loader.py
import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
if not FIRECRAWL_API_KEY:
    raise RuntimeError("FIRECRAWL_API_KEY not found in environment")

firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

def fetch_url_text(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL with BS4: {str(e)}")

def fetch_website_pages(url: str, max_pages: int = 5) -> list:
    try:
        parsed = urlparse(url)
        path = parsed.path.rstrip("/")

        if not path or path == "":
            result = firecrawl.crawl(url, limit=max_pages)
            if not result or "data" not in result or not result["data"]:
                text = fetch_url_text(url)
                if not text.strip():
                    raise ValueError("No readable content found from URL")
                return [text]

            pages_text = []
            for page in result["data"]:
                content = page.get("markdown") or page.get("content") or ""
                if content.strip():
                    pages_text.append(content)
            return pages_text
        else:
            result = firecrawl.scrape(url)
            if not result or "data" not in result:
                text = fetch_url_text(url)
                if not text.strip():
                    raise ValueError("No readable content found from URL")
                return [text]

            data = result["data"]
            content = data.get("markdown") or data.get("content") or ""
            if not content.strip():
                text = fetch_url_text(url)
                if not text.strip():
                    raise ValueError("No readable content found from URL")
                return [text]

            return [content]

    except Exception as e:
        try:
            text = fetch_url_text(url)
            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail=f"Could not fetch content from URL: {str(e)}"
                )
            return [text]
        except Exception as inner:
            raise HTTPException(
                status_code=400,
                detail=f"Firecrawl and BS4 both failed: {str(inner)}"
            )
