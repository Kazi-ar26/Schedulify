"""
Schedulify Notification ORM Model

Stores application notifications.

Examples:
- Task reminders
- Schedule updates
- System alerts
- Productivity messages
"""


from datetime import datetime, timezone

import enum


from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    Enum,
    ForeignKey
)


from sqlalchemy.orm import relationship


from Database.database import Base



# -------------------------------------------------
# Notification Type
# -------------------------------------------------

class NotificationType(enum.Enum):

    TASK = "task"

    SCHEDULE = "schedule"

    PRODUCTIVITY = "productivity"

    SYSTEM = "system"



# -------------------------------------------------
# Notification Priority
# -------------------------------------------------

class NotificationPriority(enum.Enum):

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"



# -------------------------------------------------
# Notification Model
# -------------------------------------------------

class Notification(Base):

    __tablename__ = "notifications"



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

        nullable=False

    )


    user = relationship(

        "User",

        back_populates="notifications"

    )



    # -------------------------------------------------
    # Notification Content
    # -------------------------------------------------

    title = Column(

        String(255),

        nullable=False

    )


    message = Column(

        Text,

        nullable=False

    )



    # -------------------------------------------------
    # Classification
    # -------------------------------------------------

    notification_type = Column(

        Enum(NotificationType),

        default=NotificationType.SYSTEM,

        nullable=False

    )


    priority = Column(

        Enum(NotificationPriority),

        default=NotificationPriority.MEDIUM,

        nullable=False

    )



    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    is_read = Column(

        Boolean,

        default=False,

        nullable=False

    )



    # -------------------------------------------------
    # Timestamp
    # -------------------------------------------------

    created_at = Column(

        DateTime,

        default=lambda:
            datetime.now(timezone.utc),

        nullable=False

    )


    read_at = Column(

        DateTime,

        nullable=True

    )



    # -------------------------------------------------
    # Helper Methods
    # -------------------------------------------------

    def mark_as_read(self):

        self.is_read = True

        self.read_at = datetime.now(
            timezone.utc
        )



    def __repr__(self):

        return (

            f"<Notification("
            f"id={self.id}, "
            f"title='{self.title}', "
            f"read={self.is_read}"
            f")>"

        )