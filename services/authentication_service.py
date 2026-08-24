"""
Schedulify Authentication Service

Responsible for:
- User authentication
- User registration
- Password hashing
- Password verification
"""

from typing import Optional

from passlib.context import CryptContext

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.user import User, UserRole
from models.student import Student
from models.teacher import Teacher


class AuthenticationService:

    """
    Handles all authentication logic.
    """

    _password_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )


    # -------------------------------------------------
    # Password Utilities
    # -------------------------------------------------

    @classmethod
    def hash_password(
        cls,
        password: str
    ) -> str:

        return cls._password_context.hash(
            password
        )

    @classmethod
    def verify_password(
        cls,
        password: str,
        password_hash: str
    ) -> bool:

        return cls._password_context.verify(
            password,
            password_hash
        )


    # -------------------------------------------------
    # User Lookup
    # -------------------------------------------------

    @classmethod
    def get_user_by_email(
        cls,
        session: Session,
        email: str
    ) -> Optional[User]:

        statement = select(User).where(
            User.email == email
        )

        result = session.execute(statement)

        return result.scalar_one_or_none()


    # -------------------------------------------------
    # Authentication
    # -------------------------------------------------

    @classmethod
    def authenticate_user(
        cls,
        session: Session,
        email: str,
        password: str
    ) -> Optional[User]:

        user = cls.get_user_by_email(
            session,
            email
        )

        if user is None:
            return None

        if not user.is_active:
            return None

        if not cls.verify_password(
            password,
            user.password_hash
        ):
            return None

        return user


    # -------------------------------------------------
    # Registration
    # -------------------------------------------------

    @classmethod
    def register_user(
        cls,
        session: Session,
        *,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: UserRole
    ) -> User:

        existing_user = cls.get_user_by_email(
            session,
            email
        )

        if existing_user is not None:
            raise ValueError(
                "An account with this email "
                "already exists."
            )

        user = User(
            email=email,
            password_hash=cls.hash_password(
                password
            ),
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active=True
        )

        session.add(user)
        session.flush()

        if role == UserRole.STUDENT:
            student = Student(user_id=user.id)
            session.add(student)

        elif role == UserRole.TEACHER:
            teacher = Teacher(user_id=user.id)
            session.add(teacher)

        try:
            session.commit()
            session.refresh(user)

        except IntegrityError:
            session.rollback()
            raise ValueError(
                "An account with this email "
                "already exists."
            )

        return user
