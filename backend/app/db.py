import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


def get_engine():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return create_engine(url, pool_pre_ping=True)


engine = None
SessionLocal = None


def init_db():
    """Create the engine and any missing tables. Safe to run repeatedly."""
    global engine, SessionLocal
    from . import models  # noqa: F401  (registers the tables on Base)

    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    return engine
