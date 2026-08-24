"""
Schedulify Settings Controller

Handles settings via the backend API.
"""

from api_client.settings_api import get_settings, update_settings
from api_client.client import APIError


class SettingsController:

    def __init__(self, session=None):
        self.session = session

    def get_settings(self, user_id: int = None) -> dict:
        """Get user settings via API."""
        try:
            return get_settings()
        except APIError:
            return {
                "dark_mode": True,
                "notifications_enabled": True,
                "auto_reschedule": True,
                "default_study_duration": 60,
            }

    def save_settings(self, user_id: int = None, settings_data: dict = None) -> dict:
        """Save settings via API."""
        if settings_data is None:
            settings_data = {}

        update_kwargs = {}
        if "theme" in settings_data:
            update_kwargs["dark_mode"] = (
                settings_data["theme"].lower() == "dark"
            )
        if "notifications" in settings_data:
            update_kwargs["notifications_enabled"] = settings_data["notifications"]

        return update_settings(**update_kwargs)

    def update_theme(self, user_id: int = None, theme: str = "dark") -> dict:
        return update_settings(dark_mode=(theme.lower() == "dark"))

    def update_notifications(self, user_id: int = None, enabled: bool = True) -> dict:
        return update_settings(notifications_enabled=enabled)
