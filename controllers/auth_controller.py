"""
Schedulify Authentication Controller

Responsible for:
- Login flow
- Registration flow
- Session user handling

Communicates with:
- AuthenticationService
"""


from typing import Optional


from sqlalchemy.orm import Session


from models.user import User, UserRole


from services.authentication_service import (
    AuthenticationService
)



class AuthController:



    def __init__(
        self,
        session: Session
    ):

        self.session = session

        self.auth_service = AuthenticationService()



    # -------------------------------------------------
    # Login
    # -------------------------------------------------

    def login(
        self,
        email: str,
        password: str
    ) -> Optional[User]:


        user = (

            self.auth_service
            .authenticate_user(
                self.session,
                email,
                password
            )

        )


        return user



    # -------------------------------------------------
    # Register
    # -------------------------------------------------

    def register_student(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str
    ) -> User:


        user = (

            self.auth_service
            .register_user(
                role=UserRole.STUDENT,
                session=self.session,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            

            )

        )


        return user



    def register_teacher(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str
    ) -> User:


        user = (

            self.auth_service
            .register_user(
                role=UserRole.TEACHER,
                session=self.session,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            )


        return user



    # -------------------------------------------------
    # Session Helpers
    # -------------------------------------------------

    @staticmethod
    def get_dashboard_type(
        user: User
    ) -> str:


        if user.role == UserRole.STUDENT:

            return "student"



        if user.role == UserRole.TEACHER:

            return "teacher"



        return "admin"