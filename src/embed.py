import json
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import settings


def build_index() -> int:
    """
    Create embeddings for each processed document and save:
    - embeddings.npy (float32, normalized)
    - metadata.json (doc fields)
    Returns number of documents indexed.
    """
    settings.INDEX_DIR.mkdir(parents=True, exist_ok=True)
    if not settings.DOCS_PROCESSED_PATH.exists():
        raise FileNotFoundError("Processed docs not found. Run: python -m src.cli preprocess")

    model = SentenceTransformer(settings.EMBED_MODEL_NAME)

    docs = []
    texts = []
    with settings.DOCS_PROCESSED_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            docs.append(d)
            texts.append(f"{d['title']}\n{d['text']}")

    emb = model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=True
    )
    emb = np.array(emb, dtype=np.float32)

    np.save(settings.EMBEDDINGS_PATH, emb)
    with settings.METADATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    return len(docs)
