"""
Schedulify Database Session Manager

Handles:
- Creating database sessions
- Managing transactions
- Commit / rollback operations
- Safe database interaction
"""

import logging
from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError

from Database.database import SessionLocal



# -------------------------------------------------
# Session Generator
# -------------------------------------------------

def create_session():
    """
    Creates and returns a SQLAlchemy database session.

    Used when manual session control is required.

    Example:

        session = create_session()

        users = session.query(User).all()

        session.close()
    """

    return SessionLocal()



# -------------------------------------------------
# Context Managed Session
# -------------------------------------------------

@contextmanager
def database_session():
    """
    Provides a safe database session.

    Automatically:
    - Opens session
    - Commits changes
    - Rolls back on errors
    - Closes connection

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
# Transaction Helper
# -------------------------------------------------

def commit_transaction(session):
    """
    Commits active database changes.

    Used when explicit transaction control
    is required.
    """

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
    """
    Cancels pending database changes.
    """

    try:

        session.rollback()


    except SQLAlchemyError as error:

        logging.error(
            f"Rollback failed: {error}"
        )

        raise