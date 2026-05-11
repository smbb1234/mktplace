from __future__ import annotations

from typing import Any, Optional

from src.shared.config.settings import get_settings


def get_chroma_client() -> Optional[Any]:
    settings = get_settings()
    if not settings.chroma_enabled:
        return None
    try:
        import chromadb

        client = chromadb.Client()
        return client
    except Exception:
        # chroma not available or failed to initialize; return None
        return None
from __future__ import annotations

from typing import Optional
import logging

log = logging.getLogger(__name__)


def get_chroma_client(*, enabled: bool, persist_directory: str | None = None):
    """Return a configured ChromaDB client if enabled, otherwise None.

    Parameters
    - enabled: Toggle for enabling ChromaDB client
    - persist_directory: Optional path for local persistence
    """
    if not enabled:
        return None
    try:
        import chromadb
        from chromadb.config import Settings as ChromaSettings
    except Exception:
        log.warning("ChromaDB client not available; skipping initialization")
        return None

    settings = {}
    if persist_directory:
        settings = dict(chroma_db_impl="duckdb+parquet", persist_directory=str(persist_directory))
    try:
        client = chromadb.Client(settings=ChromaSettings(**settings))
        try:
            client.persist()
        except Exception:
            # persist may not be strictly necessary
            log.debug("Chroma persist call failed during init", exc_info=True)
        return client
    except Exception:
        log.exception("Failed to initialize ChromaDB client")
        return None
