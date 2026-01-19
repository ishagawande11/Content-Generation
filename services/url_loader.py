from urllib.parse import urlparse
from fastapi import HTTPException
import requests
from bs4 import BeautifulSoup
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
if not FIRECRAWL_API_KEY:
    raise RuntimeError("FIRECRAWL_API_KEY not found in environment")

firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

def fetch_url_text(url: str) -> str:
    """Fallback text fetch using requests + BS4"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

def fetch_website_pages(url: str, max_pages: int = 5) -> list:
    """
    Fetch pages from a URL using Firecrawl.
    Returns a list of page texts.
    """
    try:
        parsed = urlparse(url)
        path = parsed.path.rstrip("/")

        if not path or path == "":
            result = firecrawl.crawl(url, limit=max_pages)
            if not result or "data" not in result or not result["data"]:
                return [fetch_url_text(url)]
            pages_text = []
            for page in result["data"]:
                content = page.get("markdown") or page.get("content") or ""
                if content.strip():
                    pages_text.append(content)
            return pages_text
        else:
                result = firecrawl.scrape(url)
                if not result or "data" not in result:
                    return [fetch_url_text(url)]
                data = result["data"]
                content = data.get("markdown") or data.get("content") or ""
                return [content] if content.strip() else [fetch_url_text(url)]
    except Exception as e:
             raise HTTPException(status_code=400, detail=f"Failed to fetch website pages: {str(e)}")
