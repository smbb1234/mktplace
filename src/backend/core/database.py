from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.shared.config.settings import get_settings

settings = get_settings()

# echo=False to keep output quiet for tests; change as needed
engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db_session():
    return SessionLocal()


from typing import Iterator


def get_db() -> Iterator[Session]:
    """Provide a FastAPI-compatible generator dependency for DB sessions.

    FastAPI expects dependencies that use `yield`, not contextmanager objects.
    Returning a generator allows FastAPI to properly enter/exit the dependency
    and handle exceptions.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
