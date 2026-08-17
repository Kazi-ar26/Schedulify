"""
Schedulify Settings Controller

Handles:

- User settings management
- Theme preferences
- Application preferences

Connects:
UI → Controller → SettingsService
"""

from sqlalchemy.orm import Session

from models.user import User
from models.setting import Setting

from services.settings_service import SettingsService


class SettingsController:

    def __init__(
        self,
        session: Session
    ):

        self.session = session

        self.settings_service = SettingsService()


    # -------------------------------------------------
    # Get User Settings
    # -------------------------------------------------

    def get_settings(
        self,
        user: User
    ) -> Setting:

        settings = (

            self.settings_service
            .get_user_settings(
                self.session,
                user
            )

        )

        # Create settings if this user doesn't have any yet
        if settings is None:

            settings = (

                self.settings_service
                .create_default_settings(
                    self.session,
                    user
                )

            )

        return settings


    # -------------------------------------------------
    # Update All Settings
    # -------------------------------------------------

    def save_settings(
        self,
        user: User,
        settings_data: dict
    ) -> Setting:

        settings = self.get_settings(
            user
        )

        theme = settings_data.get(
            "theme",
            "dark"
        )

        notifications = settings_data.get(
            "notifications",
            True
        )

        dark_mode = (
            theme.lower() == "dark"
        )

        return (
            self.settings_service
            .update_settings(
                self.session,
                settings,
                dark_mode=dark_mode,
                notifications_enabled=notifications
            )
        )


    # -------------------------------------------------
    # Update Theme
    # -------------------------------------------------

    def update_theme(
        self,
        user: User,
        theme: str
    ) -> Setting:

        settings = self.get_settings(
            user
        )

        dark_mode = (
            theme.lower() == "dark"
        )

        return (

            self.settings_service
            .update_settings(
                self.session,
                settings,
                dark_mode=dark_mode
            )

        )


    # -------------------------------------------------
    # Update Notifications
    # -------------------------------------------------

    def update_notifications(
        self,
        user: User,
        enabled: bool
    ) -> Setting:

        settings = self.get_settings(
            user
        )

        return (

            self.settings_service
            .update_settings(
                self.session,
                settings,
                notifications_enabled=enabled
            )

        )


    # -------------------------------------------------
    # Update General Preferences
    # -------------------------------------------------

    def update_preferences(
        self,
        user: User,
        preferences: dict
    ) -> Setting:

        settings = self.get_settings(
            user
        )

        return (

            self.settings_service
            .update_settings(
                self.session,
                settings,
                **preferences
            )

        )