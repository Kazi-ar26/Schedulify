"""
Service Layer Tests

Tests:
- Task service
- Notification service
- Analytics service
- Wellbeing service
- Settings service
- API client auth
"""

import pytest
from unittest.mock import patch, MagicMock

from models.user import User, UserRole
from models.student import Student
from models.task import Task, TaskPriority, TaskStatus

from services.task_service import TaskService
from services.notification_service import NotificationService
from services.analytics_service import AnalyticsService
from services.wellbeing_service import WellbeingService
from services.settings_service import SettingsService
from services.scheduler_service import SchedulerService


# -------------------------------------------------
# Fixtures
# -------------------------------------------------

@pytest.fixture
def student(session):
    """Creates a test student."""
    user = User(
        first_name="Service",
        last_name="Tester",
        email="service_tester@test.com",
        password_hash="hash",
        role=UserRole.STUDENT
    )

    session.add(user)
    session.flush()

    student = Student(user_id=user.id)
    session.add(student)
    session.commit()
    session.refresh(student)

    return student


# -------------------------------------------------
# Task Service Tests
# -------------------------------------------------

def test_create_task(session, student):
    task = TaskService.create_task(
        session,
        student=student,
        title="Complete Physics Revision",
        description="Chapter revision",
        priority=TaskPriority.HIGH
    )

    assert task is not None
    assert task.title == "Complete Physics Revision"
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.PENDING


def test_get_student_tasks(session, student):
    TaskService.create_task(session, student=student, title="Task 1")
    TaskService.create_task(session, student=student, title="Task 2")

    tasks = TaskService.get_student_tasks(session, student)
    assert len(tasks) == 2


def test_mark_completed(session, student):
    task = TaskService.create_task(session, student=student, title="Test Task")
    completed = TaskService.mark_completed(session, task)
    assert completed.status == TaskStatus.COMPLETED


def test_delete_task(session, student):
    task = TaskService.create_task(session, student=student, title="To Delete")
    TaskService.delete_task(session, task)
    remaining = TaskService.get_student_tasks(session, student)
    assert len(remaining) == 0


# -------------------------------------------------
# Notification Service Tests
# -------------------------------------------------

def test_create_notification(session, student):
    notification = NotificationService.create_notification(
        session,
        user=student.user,
        title="Task Reminder",
        message="Complete assignment"
    )

    assert notification is not None
    assert notification.title == "Task Reminder"
    assert notification.is_read is False


def test_get_user_notifications(session, student):
    NotificationService.create_notification(
        session, user=student.user, title="N1", message="msg1"
    )
    NotificationService.create_notification(
        session, user=student.user, title="N2", message="msg2"
    )

    notifications = NotificationService.get_user_notifications(
        session, student.user
    )
    assert len(notifications) == 2


def test_mark_all_read(session, student):
    NotificationService.create_notification(
        session, user=student.user, title="Unread", message="msg"
    )
    NotificationService.mark_all_as_read(session, student.user)

    unread = NotificationService.get_unread_notifications(session, student.user)
    assert len(unread) == 0


# -------------------------------------------------
# Analytics Service Tests
# -------------------------------------------------

def test_create_productivity_record(session, student):
    record = AnalyticsService.create_productivity_record(
        session,
        student=student,
        focus_minutes=120,
        completed_tasks=3,
        missed_tasks=1
    )

    assert record is not None
    assert record.focus_minutes == 120
    assert record.productivity_score == 75.0


def test_generate_student_summary(session, student):
    summary = AnalyticsService.generate_student_summary(session, student)

    assert isinstance(summary, dict)
    assert "total_tasks" in summary
    assert "completion_rate" in summary
    assert "total_focus_minutes" in summary


def test_get_student_productivity(session, student):
    AnalyticsService.create_productivity_record(
        session, student=student, focus_minutes=60,
        completed_tasks=2, missed_tasks=0
    )

    records = AnalyticsService.get_student_productivity(session, student)
    assert len(records) == 1
    assert records[0].focus_minutes == 60


# -------------------------------------------------
# Wellbeing Service Tests
# -------------------------------------------------

def test_workload_level_low(session, student):
    level = WellbeingService.calculate_workload_level(session, student)
    assert level == "LOW"


def test_workload_level_high(session, student):
    for i in range(12):
        TaskService.create_task(session, student=student, title=f"Task {i}")

    level = WellbeingService.calculate_workload_level(session, student)
    assert level == "HIGH"


def test_generate_recommendations(session, student):
    recs = WellbeingService.generate_recommendations(session, student)
    assert isinstance(recs, list)
    assert len(recs) > 0


def test_generate_student_insights(session, student):
    insights = WellbeingService.generate_student_insights(session, student)

    assert isinstance(insights, dict)
    assert "workload_level" in insights
    assert "consistency_score" in insights
    assert "recommendations" in insights


# -------------------------------------------------
# Settings Service Tests
# -------------------------------------------------

def test_create_default_settings(session, student):
    settings = SettingsService.create_default_settings(session, student.user)

    assert settings is not None
    assert settings.dark_mode is True
    assert settings.notifications_enabled is True


def test_get_settings(session, student):
    SettingsService.create_default_settings(session, student.user)
    settings = SettingsService.get_user_settings(session, student.user)

    assert settings is not None
    assert settings.dark_mode is True


def test_update_settings(session, student):
    settings = SettingsService.create_default_settings(session, student.user)
    updated = SettingsService.update_settings(
        session, settings, dark_mode=False
    )

    assert updated.dark_mode is False


# -------------------------------------------------
# API Client Tests
# -------------------------------------------------

def test_api_client_auth_flow():
    """API client auth operations don't crash."""
    from api_client.client import save_token, load_token, clear_token

    save_token("test-token-123", {"email": "test@test.com"})
    assert load_token() == "test-token-123"

    clear_token()
    assert load_token() is None
