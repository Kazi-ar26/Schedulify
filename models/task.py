"""
Schedulify Task ORM Model

Stores student tasks.

Connected with:
- Student
- Schedule system
"""


from datetime import datetime, timezone

import enum


from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Enum,
    ForeignKey
)


from sqlalchemy.orm import relationship


from Database.database import Base



# -------------------------------------------------
# Task Status
# -------------------------------------------------

class TaskStatus(enum.Enum):

    PENDING = "pending"

    COMPLETED = "completed"

    MISSED = "missed"



# -------------------------------------------------
# Task Priority
# -------------------------------------------------

class TaskPriority(enum.Enum):

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"



# -------------------------------------------------
# Task Model
# -------------------------------------------------

class Task(Base):

    __tablename__ = "tasks"



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

        back_populates="tasks"

    )



    # -------------------------------------------------
    # Task Information
    # -------------------------------------------------

    title = Column(

        String(255),

        nullable=False

    )


    description = Column(

        Text,

        nullable=True

    )


    category = Column(

        String(100),

        nullable=True

    )


    priority = Column(

        Enum(TaskPriority),

        default=TaskPriority.MEDIUM,

        nullable=False

    )


    estimated_duration = Column(

        Integer,

        default=60,

        nullable=False

    )


    due_date = Column(

        DateTime,

        nullable=True

    )



    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    status = Column(

        Enum(TaskStatus),

        default=TaskStatus.PENDING,

        nullable=False

    )



    # -------------------------------------------------
    # Schedule Relationship
    # -------------------------------------------------

    schedule = relationship(

        "Schedule",

        back_populates="task",

        uselist=False,

        cascade="all, delete-orphan"

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

        self.status = TaskStatus.COMPLETED



    def mark_missed(self):

        self.status = TaskStatus.MISSED



    def __repr__(self):

        return (

            f"<Task("
            f"id={self.id}, "
            f"title='{self.title}', "
            f"status='{self.status.value}'"
            f")>"

        )