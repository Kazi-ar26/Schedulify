"""
Schedulify Database Core

Responsible for:
- Creating SQLAlchemy engine
- Defining ORM Base
- Creating session factory
- Managing database connection settings
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

"""
All ORM models inherit from this Base.

Example:

class User(Base):
    __tablename__ = "users"

"""

Base = declarative_base()



# -------------------------------------------------
# Engine Creation
# -------------------------------------------------

try:

    engine = create_engine(

        DATABASE_URL,

        pool_size=10,

        max_overflow=20,

        pool_pre_ping=True,

        echo=False

    )


    logging.info(
        "SQLAlchemy engine created successfully."
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
    Creates database tables.

    Used only for development/testing.

    Production deployments should use Alembic migrations.
    """

    Base.metadata.create_all(
        bind=engine
    )


    logging.info(
        "Database tables initialized."
    )



# -------------------------------------------------
# Database Health Check
# -------------------------------------------------

def test_database_connection() -> bool:
    """
    Checks MySQL connection status.
    """

    try:

        with engine.connect():

            logging.info(
                "MySQL database connection successful."
            )

            return True


    except Exception as error:

        logging.error(
            f"MySQL connection failed: {error}"
        )

        return False

def init_database():

    Base.metadata.create_all(
        bind=engine
    )