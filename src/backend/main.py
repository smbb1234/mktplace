from __future__ import annotations

from fastapi import FastAPI

from src.shared.config.settings import get_settings
from src.backend.startup import attach_startup
from fastapi import APIRouter

# register API routers
from src.backend.api.catalog import router as catalog_router
from src.backend.api.enquiries import router as enquiries_router

app = FastAPI(title="AI Car Buying Assistant Backend", version="0.1.0")

# attach startup handlers (load catalog, optional vectorstore)
attach_startup(app)

# include routers
app.include_router(catalog_router)
app.include_router(enquiries_router)


@app.get("/health")
def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "env": "docker-compose",
        "fastapi_host": settings.fastapi_host,
        "fastapi_port": str(settings.fastapi_port),
    }
