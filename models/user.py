"""
Schedulify User ORM Model

Represents application users.

Users can be:
- Students
- Teachers

Handles:
- Authentication identity
- Account status
- User relationships
"""


from datetime import datetime, timezone

import enum


from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum
)


from sqlalchemy.orm import relationship


from Database.database import Base



# -------------------------------------------------
# User Roles
# -------------------------------------------------

class UserRole(enum.Enum):

    STUDENT = "student"

    TEACHER = "teacher"




# -------------------------------------------------
# User Model
# -------------------------------------------------

class User(Base):

    __tablename__ = "users"



    # -------------------------------------------------
    # Primary Key
    # -------------------------------------------------

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )



    # -------------------------------------------------
    # Authentication
    # -------------------------------------------------

    email = Column(

        String(255),

        unique=True,

        nullable=False,

        index=True

    )


    password_hash = Column(

        String(255),

        nullable=False

    )



    # -------------------------------------------------
    # Personal Information
    # -------------------------------------------------

    first_name = Column(

        String(100),

        nullable=False

    )


    last_name = Column(

        String(100),

        nullable=False

    )



    # -------------------------------------------------
    # Role
    # -------------------------------------------------

    role = Column(

        Enum(UserRole),

        nullable=False

    )



    # -------------------------------------------------
    # Account Status
    # -------------------------------------------------

    is_active = Column(

        Boolean,

        default=True,

        nullable=False

    )



    # -------------------------------------------------
    # Relationships
    # -------------------------------------------------

    student_profile = relationship(

        "Student",

        back_populates="user",

        uselist=False,

        cascade="all, delete-orphan"

    )


    teacher_profile = relationship(

        "Teacher",

        back_populates="user",

        uselist=False,

        cascade="all, delete-orphan"

    )


    notifications = relationship(

        "Notification",

        back_populates="user",

        cascade="all, delete-orphan"

    )


    settings = relationship(

        "Setting",

        back_populates="user",

        uselist=False,

        cascade="all, delete-orphan"

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

            f"<User("
            f"id={self.id}, "
            f"email='{self.email}', "
            f"role='{self.role.value}'"
            f")>"

        )