"""
Schedulify Calendar Event ORM Model

Handles:
- Calendar entries
- Reminders
- Meetings
- Academic events
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
# Event Type
# -------------------------------------------------

class EventType(enum.Enum):

    TASK = "task"

    CLASS = "class"

    MEETING = "meeting"

    EXAM = "exam"

    PERSONAL = "personal"



# -------------------------------------------------
# Calendar Event Model
# -------------------------------------------------

class CalendarEvent(Base):

    __tablename__ = "calendar_events"



    # -------------------------------------------------
    # Primary Key
    # -------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )



    # -------------------------------------------------
    # Student Relationship
    # -------------------------------------------------

    student_id = Column(
        Integer,
        ForeignKey(
            "students.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    student = relationship(
        "Student",
        back_populates="calendar_events"
    )



    # -------------------------------------------------
    # Event Information
    # -------------------------------------------------

    title = Column(
        String(255),
        nullable=False
    )


    description = Column(
        Text,
        nullable=True
    )


    event_type = Column(
        Enum(EventType),
        default=EventType.PERSONAL,
        nullable=False
    )



    # -------------------------------------------------
    # Timing
    # -------------------------------------------------

    start_time = Column(
        DateTime,
        nullable=False
    )


    end_time = Column(
        DateTime,
        nullable=False
    )



    location = Column(
        String(255),
        nullable=True
    )



    # -------------------------------------------------
    # Notifications
    # -------------------------------------------------

    reminder_enabled = Column(
        Boolean,
        default=True,
        nullable=False
    )



    # -------------------------------------------------
    # Timestamps
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
            f"<CalendarEvent("
            f"id={self.id}, "
            f"title='{self.title}'"
            f")>"
        )