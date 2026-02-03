import json
import hashlib
from datetime import datetime
from typing import List
from pathlib import Path

import feedparser
import requests
from bs4 import BeautifulSoup

from .config import settings

# Reliable feeds for scraping (BBC is very stable)
DEFAULT_FEEDS = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
]


def _safe_mkdirs():
    settings.RAW_DIR.mkdir(parents=True, exist_ok=True)


def _hash_id(url: str) -> str:
    return hashlib.md5(url.encode("utf-8")).hexdigest()


def _extract_article_text(url: str, timeout: int = 15) -> str:
    """
    Simple HTML-to-text extraction: concatenate paragraph text.
    This is intentionally lightweight for a class project.
    """
    r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    text = "\n".join([p for p in paras if len(p) > 40])
    return text.strip()


def ingest_rss(feeds: List[str] = None, limit: int = 150) -> int:
    """
    Download articles linked from RSS feeds and save to JSONL.
    Returns number of successfully ingested articles.
    """
    _safe_mkdirs()
    feeds = feeds or DEFAULT_FEEDS

    out_path: Path = settings.DOCS_RAW_PATH
    seen_urls = set()
    count = 0

    # Avoid duplicates if rerun
    if out_path.exists():
        with out_path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    if obj.get("url"):
                        seen_urls.add(obj["url"])
                except Exception:
                    continue

    with out_path.open("a", encoding="utf-8") as f:
        for feed_url in feeds:
            parsed = feedparser.parse(feed_url)
            feed_title = getattr(parsed.feed, "title", "") or feed_url

            for entry in getattr(parsed, "entries", []):
                if count >= limit:
                    break

                url = entry.get("link")
                if not url or url in seen_urls:
                    continue

                try:
                    text = _extract_article_text(url)
                    if len(text) < 400:
                        continue

                    doc = {
                        "id": _hash_id(url),
                        "title": (entry.get("title") or "").strip(),
                        "url": url,
                        "source": feed_title,
                        "published_at": entry.get("published", "") or entry.get("updated", ""),
                        "fetched_at": datetime.utcnow().isoformat(),
                        "text": text,
                    }

                    f.write(json.dumps(doc, ensure_ascii=False) + "\n")
                    seen_urls.add(url)
                    count += 1

                except Exception:
                    # Production behavior: skip bad pages without crashing
                    continue

    return count
