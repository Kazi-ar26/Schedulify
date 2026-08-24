"""
Schedulify Database Core

Responsible for:
- Creating SQLAlchemy engine (MySQL with pooling, SQLite as fallback)
- Defining ORM Base
- Providing session factory
- Managing database initialization
- Providing shutdown/cleanup

Uses lazy initialization so both backend (PostgreSQL) and
desktop (SQLite/API client) can share the same models.
"""

import logging
from threading import Lock

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base


# -------------------------------------------------
# SQLAlchemy Base
# -------------------------------------------------

Base = declarative_base()


# -------------------------------------------------
# Lazy Engine Creation
# -------------------------------------------------

_engine = None
_session_factory = None
IS_MYSQL = False
_init_lock = Lock()


def initialize(url: str | None = None):
    """
    Creates the SQLAlchemy engine and session factory.

    Call once at startup. Thread-safe.
    If url is not provided, reads from config.
    """
    global _engine, _session_factory, IS_MYSQL

    with _init_lock:
        if _engine is not None:
            return

        if url is None:
            from config import get_database_url
            url = get_database_url()

        IS_MYSQL = "mysql" in url or "postgresql" in url

        engine_kwargs = {}

        if IS_MYSQL or "postgresql" in url:
            engine_kwargs["pool_size"] = 10
            engine_kwargs["max_overflow"] = 20
            engine_kwargs["pool_pre_ping"] = True
            engine_kwargs["pool_recycle"] = 3600
        else:
            engine_kwargs["connect_args"] = {
                "check_same_thread": False
            }

        _engine = create_engine(url, **engine_kwargs)
        _session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine
        )

        logging.info(
            f"Database engine created ({url.split('://')[0]})."
        )


def get_engine():
    """Returns the current engine, initializing if needed."""
    if _engine is None:
        initialize()
    return _engine


def get_session_factory():
    """Returns the session factory, initializing if needed."""
    if _session_factory is None:
        initialize()
    return _session_factory


# -------------------------------------------------
# SessionLocal (backward compat — lazy)
# -------------------------------------------------

class _SessionLocalProxy:
    """Callable proxy that defers to the real session factory."""

    def __call__(self, *args, **kwargs):
        factory = get_session_factory()
        return factory(*args, **kwargs)


SessionLocal = _SessionLocalProxy()


# -------------------------------------------------
# Database Initialization
# -------------------------------------------------

def init_database():
    """Creates all database tables."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables initialized successfully.")


def test_database_connection() -> bool:
    """Checks database connection status."""
    try:
        engine = get_engine()
        with engine.connect():
            logging.info("Database connection successful.")
            return True
    except Exception as error:
        logging.error(f"Database connection failed: {error}")
        return False


def close_engine():
    """Dispose the engine and release all connections."""
    global _engine
    if _engine is not None:
        _engine.dispose()
        logging.info("Database engine disposed.")


# -------------------------------------------------
# Backward compatibility aliases
# -------------------------------------------------

initialize_database = init_database
