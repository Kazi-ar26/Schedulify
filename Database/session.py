"""
Schedulify Database Session Manager

Handles:
- Creating database sessions
- Context-managed sessions with auto-commit/rollback
- Transaction helpers
- Safe database interaction
"""

import logging
from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError

from Database.database import SessionLocal


# -------------------------------------------------
# Context Managed Session
# -------------------------------------------------

@contextmanager
def database_session():
    """
    Provides a safe database session.

    Automatically:
    - Opens session
    - Commits on success
    - Rolls back on errors
    - Closes session in all cases

    Example:

        with database_session() as session:
            session.add(user)
    """

    session = SessionLocal()

    try:
        yield session
        session.commit()

    except SQLAlchemyError as error:
        session.rollback()
        logging.error(
            f"Database transaction failed: {error}"
        )
        raise

    finally:
        session.close()


# -------------------------------------------------
# Read-only Session (no auto-commit)
# -------------------------------------------------

@contextmanager
def readonly_session():
    """
    Provides a read-only database session.

    Does NOT auto-commit — use for queries only.

    Example:

        with readonly_session() as session:
            users = session.query(User).all()
    """

    session = SessionLocal()

    try:
        yield session

    except SQLAlchemyError as error:
        logging.error(
            f"Database read failed: {error}"
        )
        raise

    finally:
        session.close()


# -------------------------------------------------
# Transaction Helper
# -------------------------------------------------

def commit_transaction(session):
    """Commits active database changes."""

    try:
        session.commit()

    except SQLAlchemyError as error:
        session.rollback()
        logging.error(
            f"Commit failed: {error}"
        )
        raise


# -------------------------------------------------
# Rollback Helper
# -------------------------------------------------

def rollback_transaction(session):
    """Cancels pending database changes."""

    try:
        session.rollback()

    except SQLAlchemyError as error:
        logging.error(
            f"Rollback failed: {error}"
        )
        raise
