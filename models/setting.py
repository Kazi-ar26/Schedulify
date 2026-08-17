"""
Schedulify Setting ORM Model

Stores user application preferences.

Handles:
- Theme settings
- Notification preferences
- Scheduler preferences
"""


from datetime import datetime, timezone


from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)


from sqlalchemy.orm import relationship


from Database.database import Base



class Setting(Base):

    __tablename__ = "settings"



    # -------------------------------------------------
    # Primary Key
    # -------------------------------------------------

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )



    # -------------------------------------------------
    # User Relationship
    # -------------------------------------------------

    user_id = Column(

        Integer,

        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),

        unique=True,

        nullable=False

    )


    user = relationship(

        "User",

        back_populates="settings"

    )



    # -------------------------------------------------
    # Appearance
    # -------------------------------------------------

    dark_mode = Column(

        Boolean,

        default=True,

        nullable=False

    )



    # -------------------------------------------------
    # Notifications
    # -------------------------------------------------

    notifications_enabled = Column(

        Boolean,

        default=True,

        nullable=False

    )


    email_notifications = Column(

        Boolean,

        default=False,

        nullable=False

    )



    # -------------------------------------------------
    # Scheduler Preferences
    # -------------------------------------------------

    auto_reschedule = Column(

        Boolean,

        default=True,

        nullable=False

    )


    default_study_duration = Column(

        Integer,

        default=60,

        nullable=False

    )



    # -------------------------------------------------
    # Timestamp
    # -------------------------------------------------

    created_at = Column(

        DateTime,

        default=lambda: datetime.now(timezone.utc),

        nullable=False

    )


    updated_at = Column(

        DateTime,

        default=lambda: datetime.now(timezone.utc),

        onupdate=lambda: datetime.now(timezone.utc),

        nullable=False

    )



    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self):

        return (

            f"<Setting("
            f"id={self.id}, "
            f"user_id={self.user_id}"
            f")>"

        )