"""SQLAlchemy engine, session, and Base setup for PostgreSQL."""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class all future SQLAlchemy models will inherit from."""
    pass


def get_db():
    """FastAPI dependency — yields one DB session per request, closes after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_db_connection():
    """Runs a test query to confirm PostgreSQL is reachable. Called on app startup."""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))