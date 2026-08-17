"""
Schedulify Database Connection Configuration

Responsible for:
- Loading environment variables
- Creating database connection URL
- Providing database configuration safely
"""


import os
from pathlib import Path

from dotenv import load_dotenv



# -------------------------------------------------
# Environment Setup
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"


if ENV_PATH.exists():

    load_dotenv(
        ENV_PATH
    )

else:

    load_dotenv()



# -------------------------------------------------
# Database Configuration
# -------------------------------------------------

class DatabaseConfig:
    """
    Stores MySQL database configuration.

    Values are loaded from environment variables.
    """


    USER = os.getenv(
        "DB_USER",
        "root"
    )


    PASSWORD = os.getenv(
        "DB_PASSWORD",
        ""
    )


    HOST = os.getenv(
        "DB_HOST",
        "localhost"
    )


    PORT = os.getenv(
        "DB_PORT",
        "3306"
    )


    NAME = os.getenv(
        "DB_NAME",
        "schedulify"
    )



# -------------------------------------------------
# Database URL Generator
# -------------------------------------------------

def get_database_url() -> str:
    """
    Creates SQLAlchemy MySQL connection URL.

    Format:

    mysql+pymysql://user:password@host:port/database
    """

    return (
        "mysql+pymysql://"
        f"{DatabaseConfig.USER}:"
        f"{DatabaseConfig.PASSWORD}@"
        f"{DatabaseConfig.HOST}:"
        f"{DatabaseConfig.PORT}/"
        f"{DatabaseConfig.NAME}"
    )



# -------------------------------------------------
# Configuration Dictionary
# -------------------------------------------------

def get_database_settings() -> dict:
    """
    Returns database configuration.

    Used by database.py.
    """

    return {

        "user": DatabaseConfig.USER,

        "host": DatabaseConfig.HOST,

        "port": DatabaseConfig.PORT,

        "database": DatabaseConfig.NAME,

        "url": get_database_url()

    }