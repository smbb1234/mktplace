from __future__ import annotations

import logging
from typing import Any, Optional

from src.shared.config.settings import get_settings

log = logging.getLogger(__name__)


def get_chroma_client(
    *, enabled: bool | None = None, persist_directory: str | None = None
) -> Optional[Any]:
    """Return a configured ChromaDB client when vector search is enabled."""
    settings = get_settings()
    if enabled is None:
        enabled = settings.chroma_enabled
    if persist_directory is None:
        persist_directory = settings.chroma_db_path

    if not enabled:
        return None

    try:
        import chromadb
        from chromadb.config import Settings as ChromaSettings
    except Exception:
        log.warning("ChromaDB client not available; skipping initialization")
        return None

    client_settings = {}
    if persist_directory:
        client_settings = {
            "chroma_db_impl": "duckdb+parquet",
            "persist_directory": str(persist_directory),
        }

    try:
        client = chromadb.Client(settings=ChromaSettings(**client_settings))
        try:
            client.persist()
        except Exception:
            log.debug("Chroma persist call failed during init", exc_info=True)
        return client
    except Exception:
        log.exception("Failed to initialize ChromaDB client")
        return None
