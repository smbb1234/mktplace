from fastapi import FastAPI
from app.database import engine, Base

from app.routes import enquiries


def create_app() -> FastAPI:
    # ensure tables exist on startup
    Base.metadata.create_all(bind=engine)
    app = FastAPI(title="Car Buying Assistant - MVP")
    app.include_router(enquiries.router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
