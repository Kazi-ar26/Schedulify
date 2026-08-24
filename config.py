"""
Schedulify Configuration Loader

Responsible for:
- Reading config.json
- Supporting environment variable overrides for secrets
- Providing a single source of truth for app configuration

Environment variable overrides (for production / CI):
    SCHEDULIFY_DB_HOST, SCHEDULIFY_DB_PORT, SCHEDULIFY_DB_NAME,
    SCHEDULIFY_DB_USER, SCHEDULIFY_DB_PASSWORD, SCHEDULIFY_DB_URL
"""


import json
import os
from pathlib import Path


# -------------------------------------------------
# Paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

CONFIG_FILE = BASE_DIR / "config.json"


# -------------------------------------------------
# Load JSON
# -------------------------------------------------

def _load_json() -> dict:
    """Reads config.json and returns a dict."""

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE}"
        )

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


# -------------------------------------------------
# Public API
# -------------------------------------------------

_config: dict | None = None


def get_config() -> dict:
    """Returns the cached application configuration."""

    global _config

    if _config is None:
        _config = _load_json()

    return _config


def get_database_config() -> dict:
    """
    Returns database configuration with environment variable overrides.

    Priority:
        1. SCHEDULIFY_DB_URL  (full SQLAlchemy URL, production)
        2. Individual SCHEDULIFY_DB_* vars
        3. config.json values
    """

    config = get_config()
    db = config.get("database", {}).copy()

    # Full URL override (production)
    env_url = os.environ.get("SCHEDULIFY_DB_URL")
    if env_url:
        db["url"] = env_url
        db["type"] = "mysql" if "mysql" in env_url else "sqlite"
        return db

    # Individual overrides
    env_map = {
        "host": "SCHEDULIFY_DB_HOST",
        "port": "SCHEDULIFY_DB_PORT",
        "database_name": "SCHEDULIFY_DB_NAME",
        "user": "SCHEDULIFY_DB_USER",
        "password": "SCHEDULIFY_DB_PASSWORD",
    }

    for key, env_var in env_map.items():
        value = os.environ.get(env_var)
        if value is not None:
            # Cast port to int
            if key == "port":
                value = int(value)
            db[key] = value

    return db


def get_database_url() -> str:
    """
    Builds a SQLAlchemy database URL from configuration.

    For MySQL:
        mysql+pymysql://user:password@host:port/database_name

    Falls back to local SQLite if no MySQL credentials are provided.
    """

    db_config = get_database_config()

    # If a full URL is already provided, use it directly
    if "url" in db_config:
        return db_config["url"]

    db_type = db_config.get("type", "sqlite")

    if db_type == "mysql":
        user = db_config.get("user", "root")
        password = db_config.get("password", "")
        host = db_config.get("host", "localhost")
        port = db_config.get("port", 3306)
        database_name = db_config.get("database_name", "schedulify")

        if password:
            auth = f"{user}:{password}"
        else:
            auth = user

        return (
            f"mysql+pymysql://{auth}@{host}:{port}/{database_name}"
        )

    # Fallback: local SQLite file
    sqlite_path = BASE_DIR / "data" / "schedulify.db"
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)

    return f"sqlite:///{sqlite_path}"


def reload_config() -> dict:
    """Force-reloads the configuration from disk."""

    global _config
    _config = _load_json()
    return _config
