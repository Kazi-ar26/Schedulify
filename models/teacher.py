"""
Schedulify Teacher ORM Model

Stores teacher-specific information.

Connected with the User authentication model.
"""


from datetime import datetime, timezone


from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)


from sqlalchemy.orm import relationship


from Database.database import Base



class Teacher(Base):

    __tablename__ = "teachers"



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
        back_populates="teacher_profile"
    )



    # -------------------------------------------------
    # Professional Information
    # -------------------------------------------------

    school_name = Column(
        String(255),
        nullable=True
    )


    department = Column(
        String(100),
        nullable=True
    )


    subject = Column(
        String(100),
        nullable=True
    )


    employee_id = Column(
        String(100),
        unique=True,
        nullable=True
    )



    # -------------------------------------------------
    # Analytics Privacy Settings
    # -------------------------------------------------

    allow_anonymous_analytics = Column(
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
            f"<Teacher("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"subject='{self.subject}'"
            f")>"
        )