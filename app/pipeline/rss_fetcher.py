import httpx
import feedparser
import logging
from typing import List, Dict

logger = logging.getLogger("ai-system.rss")

async def fetch_rss_items(url: str, timeout: int = 15) -> List[Dict]:
    """
    Fetch RSS/Atom feed and return list of simplified items.
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.get(url)
            r.raise_for_status()
            raw = r.text
    except Exception as e:
        logger.exception("Failed to fetch RSS %s", url)
        return []

    parsed = feedparser.parse(raw)
    items = []
    for e in parsed.entries:
        items.append({
            "title": getattr(e, "title", "") or "",
            "link": getattr(e, "link", "") or "",
            "summary": getattr(e, "summary", "") or getattr(e, "description", "") or "",
            "published": getattr(e, "published", "") or ""
        })
    return items
