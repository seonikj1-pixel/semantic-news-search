import json
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import settings


def _load_index():
    emb = np.load(settings.EMBEDDINGS_PATH)
    with settings.METADATA_PATH.open("r", encoding="utf-8") as f:
        meta = json.load(f)
    return emb, meta


def search(query: str, top_k: int = 5):
    """
    Semantic search using cosine similarity (dot product on normalized vectors).
    Returns list of top_k results with score + metadata.
    """
    if not settings.EMBEDDINGS_PATH.exists() or not settings.METADATA_PATH.exists():
        raise FileNotFoundError("Index not found. Run: python -m src.cli build-index")

    model = SentenceTransformer(settings.EMBED_MODEL_NAME)
    q = model.encode([query], normalize_embeddings=True).astype(np.float32)[0]

    emb, meta = _load_index()

    scores = emb @ q  # cosine similarity because vectors are normalized
    idx = np.argsort(-scores)[:top_k]

    results = []
    for i in idx:
        d = meta[int(i)]
        results.append({
            "score": float(scores[int(i)]),
            "title": d["title"],
            "url": d["url"],
            "source": d.get("source", ""),
            "published_at": d.get("published_at", ""),
            "text": d["text"][:800] + ("..." if len(d["text"]) > 800 else ""),
        })
    return results
