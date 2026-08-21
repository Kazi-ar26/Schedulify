"""
Schedulify Database Core

Responsible for:
- Creating SQLAlchemy engine
- Defining ORM Base
- Creating session factory
- Managing database initialization
"""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from Database.connection import (
    get_database_url,
    get_database_settings
)


# -------------------------------------------------
# Database Configuration
# -------------------------------------------------

database_settings = get_database_settings()

DATABASE_URL = get_database_url()


# -------------------------------------------------
# SQLAlchemy Base
# -------------------------------------------------

Base = declarative_base()


# -------------------------------------------------
# Engine Creation
# -------------------------------------------------

try:

    engine = create_engine(
        DATABASE_URL,
        echo=False
    )

    logging.info(
        "SQLite database engine created successfully."
    )

except Exception as error:

    logging.error(
        f"Database engine creation failed: {error}"
    )

    raise


# -------------------------------------------------
# Session Factory
# -------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# -------------------------------------------------
# Database Initialization
# -------------------------------------------------

def initialize_database():
    """
    Creates all database tables.
    """

    Base.metadata.create_all(
        bind=engine
    )

    logging.info(
        "SQLite database tables initialized."
    )


def init_database():
    """
    Compatibility alias used by existing application code.
    """

    Base.metadata.create_all(
        bind=engine
    )


# -------------------------------------------------
# Database Health Check
# -------------------------------------------------

def test_database_connection() -> bool:
    """
    Checks SQLite database connection status.
    """

    try:

        with engine.connect():

            logging.info(
                "SQLite database connection successful."
            )

            return True

    except Exception as error:

        logging.error(
            f"SQLite connection failed: {error}"
        )

        return False