"""
Authentication Tests

Tests:
- User registration
- Password hashing
- Login verification
"""


import pytest


from services.authentication_service import AuthenticationService

from Database.session import get_test_session



@pytest.fixture
def auth_service():

    session = get_test_session()

    return AuthenticationService(
        session
    )



def test_register_student(
    auth_service
):


    user = auth_service.register_student(

        first_name="Test",

        last_name="Student",

        email="student@test.com",

        password="Password123"

    )


    assert user is not None

    assert user.email == "student@test.com"



def test_login_success(
    auth_service
):


    auth_service.register_student(

        first_name="Login",

        last_name="User",

        email="login@test.com",

        password="Password123"

    )


    user = auth_service.login(

        email="login@test.com",

        password="Password123"

    )


    assert user is not None



def test_login_failure(
    auth_service
):


    user = auth_service.login(

        email="wrong@test.com",

        password="wrongpassword"

    )


    assert user is None