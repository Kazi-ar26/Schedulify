"""
Schedulify Database Connection Configuration

SQLite database configuration for standalone desktop deployment.
"""

from pathlib import Path


# -------------------------------------------------
# Application Paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_FILE = DATA_DIR / "schedulify.db"


# -------------------------------------------------
# Database URL
# -------------------------------------------------

def get_database_url() -> str:
    """
    Returns the SQLAlchemy SQLite database URL.
    """

    return f"sqlite:///{DATABASE_FILE}"


# -------------------------------------------------
# Configuration Dictionary
# -------------------------------------------------

def get_database_settings() -> dict:
    """
    Returns database configuration.
    """

    return {
        "type": "sqlite",
        "database": str(DATABASE_FILE),
        "url": get_database_url()
    }