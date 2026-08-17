"""
Schedulify Schedule ORM Model

Handles:
- Task scheduling
- AI generated schedules
- Rescheduling states
"""


from datetime import datetime, timezone

import enum


from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    Enum,
    ForeignKey,
    Time
)


from sqlalchemy.orm import relationship


from Database.database import Base



# -------------------------------------------------
# Schedule Status
# -------------------------------------------------

class ScheduleStatus(enum.Enum):

    PLANNED = "planned"

    COMPLETED = "completed"

    MISSED = "missed"

    RESCHEDULED = "rescheduled"



# -------------------------------------------------
# Schedule Model
# -------------------------------------------------

class Schedule(Base):

    __tablename__ = "schedules"



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

        back_populates="schedules"

    )



    # -------------------------------------------------
    # Task Relationship
    # -------------------------------------------------

    task_id = Column(

        Integer,

        ForeignKey(
            "tasks.id",
            ondelete="CASCADE"
        ),

        nullable=False,

        unique=True

    )


    task = relationship(

        "Task",

        back_populates="schedule",

        uselist=False

    )



    # -------------------------------------------------
    # Scheduling Information
    # -------------------------------------------------

    scheduled_date = Column(

        DateTime,

        nullable=False

    )


    start_time = Column(

        Time,

        nullable=False

    )


    end_time = Column(

        Time,

        nullable=False

    )



    # -------------------------------------------------
    # AI Information
    # -------------------------------------------------

    generated_by_ai = Column(

        Boolean,

        default=False,

        nullable=False

    )



    status = Column(

        Enum(ScheduleStatus),

        default=ScheduleStatus.PLANNED,

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


    updated_at = Column(

        DateTime,

        default=lambda:
            datetime.now(timezone.utc),

        onupdate=lambda:
            datetime.now(timezone.utc),

        nullable=False

    )



    # -------------------------------------------------
    # Helper Methods
    # -------------------------------------------------

    def mark_completed(self):

        self.status = ScheduleStatus.COMPLETED



    def reschedule(self):

        self.status = ScheduleStatus.RESCHEDULED



    def __repr__(self):

        return (

            f"<Schedule("
            f"id={self.id}, "
            f"task_id={self.task_id}, "
            f"status='{self.status.value}'"
            f")>"

        )