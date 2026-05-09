"""Simple DB initialization script for local development."""

from src.backend.models.common import Base
from src.backend.core.database import engine


def init_db() -> None:
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print("Error creating database tables:", e)
        raise
