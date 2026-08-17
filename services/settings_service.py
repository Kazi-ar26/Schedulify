"""
Schedulify Setting Service

Responsible for:
- User preferences
- Application settings
- Theme configuration
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.setting import Setting
from models.user import User



class SettingsService:



    # -------------------------------------------------
    # Get Settings
    # -------------------------------------------------

    @staticmethod
    def get_user_settings(
        session: Session,
        user: User
    ) -> Optional[Setting]:


        statement = (

            select(Setting)

            .where(
                Setting.user_id == user.id
            )

        )


        return session.scalar(statement)



    # -------------------------------------------------
    # Create Default Settings
    # -------------------------------------------------

    @staticmethod
    def create_default_settings(
        session: Session,
        user: User
    ) -> Setting:


        settings = Setting(

            user_id=user.id,

            dark_mode=True,

            notifications_enabled=True,

            email_notifications=False,

            auto_reschedule=True,

            default_study_duration=60

        )


        session.add(settings)

        session.commit()

        session.refresh(settings)


        return settings



    # -------------------------------------------------
    # Update Settings
    # -------------------------------------------------

    @staticmethod
    def update_settings(
        session: Session,
        settings: Setting,
        **changes
    ) -> Setting:


        for key, value in changes.items():


            if hasattr(settings, key):

                setattr(
                    settings,
                    key,
                    value
                )


        session.commit()

        session.refresh(settings)


        return settings



    # -------------------------------------------------
    # Reset Settings
    # -------------------------------------------------

    @staticmethod
    def reset_settings(
        session: Session,
        settings: Setting
    ) -> Setting:


        settings.dark_mode = True

        settings.notifications_enabled = True

        settings.email_notifications = False

        settings.auto_reschedule = True

        settings.default_study_duration = 60


        session.commit()

        session.refresh(settings)


        return settings