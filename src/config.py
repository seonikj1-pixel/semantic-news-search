from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    # Project root = folder containing /src and /data
    PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]

    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DIR: Path = DATA_DIR / "processed"
    INDEX_DIR: Path = DATA_DIR / "index"

    DOCS_RAW_PATH: Path = RAW_DIR / "articles.jsonl"
    DOCS_PROCESSED_PATH: Path = PROCESSED_DIR / "docs.jsonl"

    EMBEDDINGS_PATH: Path = INDEX_DIR / "embeddings.npy"
    METADATA_PATH: Path = INDEX_DIR / "metadata.json"

    EMBED_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Optional (only needed if you later add OpenAI summarization)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")


settings = Settings()
