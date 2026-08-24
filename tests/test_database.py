"""
Database Tests

Tests:
- Session creation
- Model persistence
- Basic CRUD operations
"""

import pytest

from models.user import User, UserRole
from models.student import Student
from models.task import Task, TaskStatus, TaskPriority


def test_session_creation(session):
    """Database session is created successfully."""

    assert session is not None


def test_create_user(session):
    """A user can be created and persisted."""

    user = User(
        first_name="Database",
        last_name="Test",
        email="database@test.com",
        password_hash="hashed_password",
        role=UserRole.STUDENT
    )

    session.add(user)
    session.commit()

    result = (
        session.query(User)
        .filter_by(email="database@test.com")
        .first()
    )

    assert result is not None
    assert result.email == "database@test.com"
    assert result.role == UserRole.STUDENT


def test_user_persistence(session):
    """Multiple users can be stored."""

    users_before = (
        session.query(User).count()
    )

    user = User(
        first_name="Persistence",
        last_name="Check",
        email="persist@test.com",
        password_hash="hash",
        role=UserRole.TEACHER
    )

    session.add(user)
    session.commit()

    users_after = (
        session.query(User).count()
    )

    assert users_after == users_before + 1


def test_create_student_with_user(session):
    """Student profile is linked to user."""

    user = User(
        first_name="Test",
        last_name="Student",
        email="student_crud@test.com",
        password_hash="hash",
        role=UserRole.STUDENT
    )

    session.add(user)
    session.flush()

    student = Student(user_id=user.id)
    session.add(student)
    session.commit()

    assert student.user_id == user.id
    assert student.user.email == "student_crud@test.com"


def test_create_task(session):
    """A task can be created for a student."""

    user = User(
        first_name="Task",
        last_name="User",
        email="task_user@test.com",
        password_hash="hash",
        role=UserRole.STUDENT
    )

    session.add(user)
    session.flush()

    student = Student(user_id=user.id)
    session.add(student)
    session.flush()

    task = Task(
        student_id=student.id,
        title="Complete Assignment",
        priority=TaskPriority.HIGH,
        estimated_duration=90
    )

    session.add(task)
    session.commit()

    assert task.id is not None
    assert task.title == "Complete Assignment"
    assert task.status == TaskStatus.PENDING
