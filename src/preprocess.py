import json
import re
from .config import settings

_ws = re.compile(r"\s+")
_bad = re.compile(r"(Subscribe|Sign up|All rights reserved|Cookie)", re.IGNORECASE)


def clean_text(t: str) -> str:
    t = t or ""
    t = _bad.sub(" ", t)
    t = _ws.sub(" ", t).strip()
    return t


def preprocess() -> int:
    """
    Read raw JSONL articles, clean/normalize text, write processed JSONL docs.
    Returns number of processed documents.
    """
    settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    if not settings.DOCS_RAW_PATH.exists():
        raise FileNotFoundError("Raw articles not found. Run: python -m src.cli ingest")

    n = 0
    with settings.DOCS_RAW_PATH.open("r", encoding="utf-8") as fin, \
         settings.DOCS_PROCESSED_PATH.open("w", encoding="utf-8") as fout:
        for line in fin:
            obj = json.loads(line)
            title = clean_text(obj.get("title", ""))
            text = clean_text(obj.get("text", ""))

            # Filter very short pages
            if len(text) < 300:
                continue

            doc = {
                "id": obj["id"],
                "title": title,
                "text": text,
                "url": obj.get("url", ""),
                "source": obj.get("source", ""),
                "published_at": obj.get("published_at", ""),
            }
            fout.write(json.dumps(doc, ensure_ascii=False) + "\n")
            n += 1

    return n
