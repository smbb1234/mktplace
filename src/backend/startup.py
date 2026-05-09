from __future__ import annotations

from typing import Optional
import logging

from fastapi import FastAPI

from src.shared.config.settings import get_settings
from src.backend.services.inventory.catalog import get_default_catalog, InventoryCatalog
from src.backend.core.database import engine
from src.backend.models.common import Base

log = logging.getLogger(__name__)

# module-level catalog and optional vectorstore client
catalog: Optional[InventoryCatalog] = None
chroma_client = None


def _init_chroma(settings):
    try:
        import chromadb
        from chromadb.config import Settings as ChromaSettings
    except Exception:
        log.warning("ChromaDB client not available; skipping chroma initialization")
        return None

    if settings.chroma_enabled:
        # Use local persistence path when enabled
        client = chromadb.Client(settings=ChromaSettings(chroma_db_impl="duckdb+parquet", persist_directory=str(settings.chroma_db_path)))
        try:
            client.persist()
        except Exception:
            # persist may not be necessary; ignore failures
            log.debug("Chroma persist call failed during startup", exc_info=True)
        log.info("ChromaDB client initialized with persist dir %s", settings.chroma_db_path)
        return client
    return None


def attach_startup(app: FastAPI) -> None:
    settings = get_settings()

    @app.on_event("startup")
    def _startup() -> None:
        global catalog, chroma_client

        # Initialize database tables
        Base.metadata.create_all(bind=engine)
        log.info("Database tables initialized")

        log.info("Backend startup: loading inventory catalog from %s", settings.inventory_csv_path)
        try:
            catalog = get_default_catalog(csv_path=settings.inventory_csv_path)
            log.info("Loaded %d vehicles into catalog", len(catalog.list_vehicle_ids()))
        except Exception:
            log.exception("Failed to load inventory catalog")

        if settings.chroma_enabled:
            chroma_client = _init_chroma(settings)
            if chroma_client is None:
                log.warning("Chroma enabled but client failed to initialize")


def get_catalog() -> Optional[InventoryCatalog]:
    return catalog


def get_chroma_client():
    return chroma_client
