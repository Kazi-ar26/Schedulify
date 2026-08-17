"""
Schedulify Student ORM Model

Stores student-specific information.

Connected with:
- User authentication
- Tasks
- Schedules
- Calendar events
- Productivity tracking
- Analytics
"""


from datetime import datetime, timezone


from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)


from sqlalchemy.orm import relationship


from Database.database import Base



class Student(Base):

    __tablename__ = "students"



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

        back_populates="student_profile"

    )



    # -------------------------------------------------
    # Academic Information
    # -------------------------------------------------

    school_name = Column(

        String(255),

        nullable=True

    )


    grade_level = Column(

        String(50),

        nullable=True

    )


    academic_year = Column(

        String(20),

        nullable=True

    )



    # -------------------------------------------------
    # Scheduling Preferences
    # -------------------------------------------------

    preferred_study_hours = Column(

        String(100),

        nullable=True

    )


    timezone = Column(

        String(50),

        default="UTC",

        nullable=False

    )



    # -------------------------------------------------
    # Relationships
    # -------------------------------------------------

    tasks = relationship(

        "Task",

        back_populates="student",

        cascade="all, delete-orphan"

    )


    schedules = relationship(

        "Schedule",

        back_populates="student",

        cascade="all, delete-orphan"

    )


    calendar_events = relationship(

        "CalendarEvent",

        back_populates="student",

        cascade="all, delete-orphan"

    )


    productivity_records = relationship(

        "ProductivityRecord",

        back_populates="student",

        cascade="all, delete-orphan"

    )


    analytics_records = relationship(

        "AnalyticsRecord",

        back_populates="student",

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
    # Representation
    # -------------------------------------------------

    def __repr__(self):

        return (

            f"<Student("
            f"id={self.id}, "
            f"user_id={self.user_id}"
            f")>"

        )