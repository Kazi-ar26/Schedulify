"""
Schedulify Database Connection Configuration

Responsible for:
- Reading database configuration from config.py
- Building the SQLAlchemy database URL
- Supporting central MySQL or local SQLite
"""


from config import get_database_config, get_database_url


# -------------------------------------------------
# Re-exports for backward compatibility
# -------------------------------------------------

def get_database_settings() -> dict:
    """Returns database configuration dict."""

    return get_database_config()
