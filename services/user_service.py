"""
Schedulify User Service

Responsible for:
- User management
- Profile management
- Account status
- Student/Teacher profile creation
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User
from models.student import Student
from models.teacher import Teacher

from services.authentication_service import AuthenticationService


class UserService:

    # -------------------------------------------------
    # User Retrieval
    # -------------------------------------------------

    @staticmethod
    def get_user_by_id(
        session: Session,
        user_id: int
    ) -> Optional[User]:

        statement = select(User).where(
            User.id == user_id
        )

        return session.scalar(statement)

    @staticmethod
    def get_all_students(
        session: Session
    ) -> list[Student]:

        statement = select(Student)

        return list(
            session.scalars(statement).all()
        )

    @staticmethod
    def get_all_teachers(
        session: Session
    ) -> list[Teacher]:

        statement = select(Teacher)

        return list(
            session.scalars(statement).all()
        )



    # -------------------------------------------------
    # Account Status
    # -------------------------------------------------

    @staticmethod
    def activate_user(
        session: Session,
        user: User
    ) -> None:

        user.is_active = True

        session.commit()

    @staticmethod
    def deactivate_user(
        session: Session,
        user: User
    ) -> None:

        user.is_active = False

        session.commit()



    # -------------------------------------------------
    # Password
    # -------------------------------------------------

    @staticmethod
    def change_password(
        session: Session,
        user: User,
        new_password: str
    ) -> None:

        user.password_hash = (
            AuthenticationService.hash_password(
                new_password
            )
        )

        session.commit()



    # -------------------------------------------------
    # Profile Updates
    # -------------------------------------------------

    @staticmethod
    def update_user_profile(
        session: Session,
        user: User,
        *,
        first_name: str,
        last_name: str
    ) -> User:

        user.first_name = first_name
        user.last_name = last_name

        session.commit()

        session.refresh(user)

        return user



    # -------------------------------------------------
    # Student Profile
    # -------------------------------------------------

    @staticmethod
    def create_student_profile(
        session: Session,
        user: User,
        school_name: str,
        grade_level: str,
        academic_year: str
    ) -> Student:

        profile = Student(

            user_id=user.id,

            school_name=school_name,

            grade_level=grade_level,

            academic_year=academic_year

        )

        session.add(profile)

        session.commit()

        session.refresh(profile)

        return profile



    # -------------------------------------------------
    # Teacher Profile
    # -------------------------------------------------

    @staticmethod
    def create_teacher_profile(
        session: Session,
        user: User,
        school_name: str,
        department: str,
        subject: str,
        employee_id: str
    ) -> Teacher:

        profile = Teacher(

            user_id=user.id,

            school_name=school_name,

            department=department,

            subject=subject,

            employee_id=employee_id

        )

        session.add(profile)

        session.commit()

        session.refresh(profile)

        return profile



    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    @staticmethod
    def delete_user(
        session: Session,
        user: User
    ) -> None:

        session.delete(user)

        session.commit()