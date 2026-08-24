"""
Authentication Tests

Tests:
- User registration
- Password hashing
- Login verification
- Duplicate email handling
- JWT token creation/verification
"""

import pytest

from services.authentication_service import AuthenticationService
from models.user import User, UserRole
from backend.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)


def test_hash_and_verify_password():
    """Password hashing and verification work."""
    password = "SecurePass123"
    hashed = AuthenticationService.hash_password(password)

    assert hashed != password
    assert AuthenticationService.verify_password(password, hashed)
    assert not AuthenticationService.verify_password("WrongPassword", hashed)


def test_backend_password_hashing():
    """Backend password hashing works."""
    password = "TestPass456"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("Wrong", hashed)


def test_register_student(session):
    """A student can register successfully."""
    user = AuthenticationService.register_user(
        session,
        email="student@test.com",
        password="Password123",
        first_name="Test",
        last_name="Student",
        role=UserRole.STUDENT
    )

    assert user is not None
    assert user.email == "student@test.com"
    assert user.role == UserRole.STUDENT
    assert user.student_profile is not None


def test_register_teacher(session):
    """A teacher can register successfully."""
    user = AuthenticationService.register_user(
        session,
        email="teacher@test.com",
        password="Password123",
        first_name="Test",
        last_name="Teacher",
        role=UserRole.TEACHER
    )

    assert user is not None
    assert user.email == "teacher@test.com"
    assert user.role == UserRole.TEACHER
    assert user.teacher_profile is not None


def test_duplicate_email_rejected(session):
    """Registration with duplicate email raises ValueError."""
    AuthenticationService.register_user(
        session,
        email="duplicate@test.com",
        password="Password123",
        first_name="First",
        last_name="User",
        role=UserRole.STUDENT
    )

    with pytest.raises(ValueError):
        AuthenticationService.register_user(
            session,
            email="duplicate@test.com",
            password="Password456",
            first_name="Second",
            last_name="User",
            role=UserRole.STUDENT
        )


def test_login_success(session):
    """A registered user can log in."""
    AuthenticationService.register_user(
        session,
        email="login@test.com",
        password="Password123",
        first_name="Login",
        last_name="User",
        role=UserRole.STUDENT
    )

    user = AuthenticationService.authenticate_user(
        session, "login@test.com", "Password123"
    )

    assert user is not None
    assert user.email == "login@test.com"


def test_login_wrong_password(session):
    """Login with wrong password returns None."""
    AuthenticationService.register_user(
        session,
        email="wrongpw@test.com",
        password="Password123",
        first_name="Wrong",
        last_name="PW",
        role=UserRole.STUDENT
    )

    user = AuthenticationService.authenticate_user(
        session, "wrongpw@test.com", "WrongPassword"
    )

    assert user is None


def test_login_nonexistent_user(session):
    """Login with non-existent email returns None."""
    user = AuthenticationService.authenticate_user(
        session, "nobody@test.com", "Password123"
    )

    assert user is None


def test_get_user_by_email(session):
    """User lookup by email works."""
    AuthenticationService.register_user(
        session,
        email="lookup@test.com",
        password="Password123",
        first_name="Lookup",
        last_name="User",
        role=UserRole.STUDENT
    )

    found = AuthenticationService.get_user_by_email(
        session, "lookup@test.com"
    )

    assert found is not None
    assert found.first_name == "Lookup"


def test_jwt_token_creation_and_decode():
    """JWT tokens can be created and decoded."""
    token = create_access_token(data={"sub": "42"})

    payload = decode_token(token)
    assert payload["sub"] == "42"


def test_jwt_token_with_user_id(session):
    """JWT token stores user ID correctly."""
    user = AuthenticationService.register_user(
        session,
        email="jwt@test.com",
        password="Password123",
        first_name="JWT",
        last_name="User",
        role=UserRole.STUDENT
    )

    token = create_access_token(data={"sub": str(user.id)})
    payload = decode_token(token)

    assert int(payload["sub"]) == user.id
