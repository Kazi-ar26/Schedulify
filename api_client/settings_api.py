"""
Schedulify Settings API Service
"""

from api_client.client import get_client


def get_settings() -> dict:
    """Get user settings."""
    return get_client().get("/api/settings")


def update_settings(**kwargs) -> dict:
    """Update user settings."""
    data = {k: v for k, v in kwargs.items() if v is not None}
    return get_client().put("/api/settings", data)
