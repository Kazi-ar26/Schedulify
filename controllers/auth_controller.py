"""
Schedulify Authentication Controller

Handles login/registration via the backend API.
"""

from typing import Optional

from api_client.auth_api import login as api_login
from api_client.auth_api import register as api_register
from api_client.auth_api import get_me
from api_client.client import APIError


class AuthController:

    def __init__(self, session=None):
        """session parameter kept for compatibility, not used."""
        self.session = session

    # -------------------------------------------------
    # Login
    # -------------------------------------------------

    def login(self, email: str, password: str) -> Optional[dict]:
        """
        Authenticate via API.

        Returns user dict with 'id', 'email', 'first_name', etc.
        or None if login fails.
        """
        try:
            result = api_login(email, password)

            if result and "user" in result:
                user_data = result["user"]
                # Store token in the result for the caller
                user_data["_token"] = result.get("access_token")
                return user_data

            return None

        except APIError as e:
            raise Exception(str(e))

    # -------------------------------------------------
    # Registration
    # -------------------------------------------------

    def register_student(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        school_name: str = None,
        grade_level: str = None,
    ) -> dict:
        """Register a new student account."""
        try:
            result = api_register(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role="student",
                school_name=school_name,
                grade_level=grade_level,
            )

            if result and "user" in result:
                return result["user"]

            raise Exception("Registration failed.")

        except APIError as e:
            raise Exception(str(e))

    def register_teacher(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
    ) -> dict:
        """Register a new teacher account."""
        try:
            result = api_register(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role="teacher",
            )

            if result and "user" in result:
                return result["user"]

            raise Exception("Registration failed.")

        except APIError as e:
            raise Exception(str(e))

    # -------------------------------------------------
    # Session Helpers
    # -------------------------------------------------

    @staticmethod
    def get_dashboard_type(user: dict) -> str:
        role = user.get("role", "")
        if role == "student":
            return "student"
        if role == "teacher":
            return "teacher"
        return "admin"
