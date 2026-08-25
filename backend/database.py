"""
Schedulify Backend Database

Creates its own PostgreSQL engine and session factory,
reusing the same ORM models defined in models/.
"""

import os
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Database.database import Base

load_dotenv()


# -------------------------------------------------
# PostgreSQL Engine
# -------------------------------------------------

def _get_database_url() -> str:
    """
    Builds PostgreSQL connection URL from environment variables.

    Expects:
        DATABASE_URL  (full URL, e.g. postgresql://...@.../schedulify)
    or individual:
        SCHEDULIFY_DB_HOST, SCHEDULIFY_DB_PORT,
        SCHEDULIFY_DB_NAME, SCHEDULIFY_DB_USER, SCHEDULIFY_DB_PASSWORD
    """
    full_url = os.environ.get("DATABASE_URL")
    if full_url:
        return full_url

    host = os.environ.get("SCHEDULIFY_DB_HOST", "localhost")
    port = os.environ.get("SCHEDULIFY_DB_PORT", "5432")
    name = os.environ.get("SCHEDULIFY_DB_NAME", "schedulify")
    user = os.environ.get("SCHEDULIFY_DB_USER", "postgres")
    password = os.environ.get("SCHEDULIFY_DB_PASSWORD", "")

    if password:
        auth = f"{user}:{password}"
    else:
        auth = user

    return f"postgresql://{auth}@{host}:{port}/{name}"


DATABASE_URL = _get_database_url()

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# -------------------------------------------------
# Table Creation
# -------------------------------------------------

def init_db():
    """Create all tables in PostgreSQL."""
    # Import all models so Base.metadata knows about them
    import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    logging.info("Backend database tables initialized.")


def get_db():
    """
    FastAPI dependency: yields a DB session and closes it after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
