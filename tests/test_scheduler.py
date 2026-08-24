"""
Scheduler Tests

Tests:
- Schedule generation
- Task prioritization
- Automatic rescheduling
- Conflict detection
"""

import pytest
from datetime import datetime, timedelta

from ai_engine.smart_scheduler import SmartScheduler
from ai_engine.rescheduler import Rescheduler
from models.task import Task, TaskPriority, TaskStatus
from models.user import User, UserRole
from models.student import Student


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def _make_task(
    session,
    student,
    title,
    priority,
    duration,
    due_date=None
) -> Task:
    """Creates a real Task in the database."""

    task = Task(
        student_id=student.id,
        title=title,
        priority=priority,
        estimated_duration=duration,
        due_date=due_date,
        status=TaskStatus.PENDING
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@pytest.fixture
def student(session):
    """Creates a test student."""

    user = User(
        first_name="Scheduler",
        last_name="Test",
        email="scheduler@test.com",
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


@pytest.fixture
def scheduler():
    return SmartScheduler()


@pytest.fixture
def rescheduler():
    return Rescheduler()


# -------------------------------------------------
# Smart Scheduler Tests
# -------------------------------------------------

def test_scheduler_generates_plan(
    scheduler,
    session,
    student
):

    tasks = [
        _make_task(
            session, student,
            "Physics Revision",
            TaskPriority.HIGH,
            120
        ),
        _make_task(
            session, student,
            "Math Practice",
            TaskPriority.MEDIUM,
            60
        ),
    ]

    result = scheduler.generate_schedule(
        tasks,
        datetime.now()
    )

    assert result is not None
    assert len(result) == 2
    assert all(
        "task" in item
        and "start_time" in item
        and "end_time" in item
        for item in result
    )


def test_high_priority_task_first(
    scheduler,
    session,
    student
):

    low_task = _make_task(
        session, student,
        "Easy Task",
        TaskPriority.LOW,
        30
    )

    high_task = _make_task(
        session, student,
        "Important Task",
        TaskPriority.HIGH,
        90
    )

    result = scheduler.generate_schedule(
        [low_task, high_task],
        datetime.now()
    )

    # High priority should be scheduled first
    assert (
        result[0]["task"].id == high_task.id
    )


def test_schedule_respects_working_hours(
    scheduler,
    session,
    student
):

    tasks = [
        _make_task(
            session, student,
            f"Task {i}",
            TaskPriority.MEDIUM,
            60
        )
        for i in range(16)
    ]

    result = scheduler.generate_schedule(
        tasks,
        datetime.now()
    )

    # All tasks should be scheduled within working hours
    for item in result:
        assert (
            item["start_time"].hour
            >= scheduler.daily_start_hour
        )


def test_detect_conflicts(scheduler):
    """Conflict detection works on schedule dicts."""

    now = datetime.now()

    schedules = [
        {
            "start_time": now,
            "end_time": now + timedelta(hours=2),
            "task": "A"
        },
        {
            "start_time": now + timedelta(hours=1),
            "end_time": now + timedelta(hours=3),
            "task": "B"
        },
    ]

    conflicts = scheduler.detect_conflicts(schedules)

    assert len(conflicts) == 1


def test_no_conflicts(scheduler):
    """Non-overlapping schedules have no conflicts."""

    now = datetime.now()

    schedules = [
        {
            "start_time": now,
            "end_time": now + timedelta(hours=1),
            "task": "A"
        },
        {
            "start_time": now + timedelta(hours=2),
            "end_time": now + timedelta(hours=3),
            "task": "B"
        },
    ]

    conflicts = scheduler.detect_conflicts(schedules)

    assert len(conflicts) == 0


# -------------------------------------------------
# Rescheduler Tests
# -------------------------------------------------

def test_reschedule_task(
    rescheduler,
    session,
    student
):

    task = _make_task(
        session, student,
        "Assignment",
        TaskPriority.HIGH,
        60
    )

    now = datetime.now()

    existing = [
        {
            "start_time": now,
            "end_time": now + timedelta(hours=1)
        }
    ]

    result = rescheduler.reschedule_task(
        task,
        existing,
        now
    )

    assert result is not None
    assert "start_time" in result
    assert "end_time" in result
    assert result["task"].id == task.id


def test_reschedule_no_slot_available(
    rescheduler,
    session,
    student
):

    task = _make_task(
        session, student,
        "Long Task",
        TaskPriority.MEDIUM,
        60
    )

    now = datetime.now()

    # Fill every 30-min slot from midnight to cover
    # the full working window for 7 days.
    # The rescheduler resets to working_start_hour,
    # so we must fill from 00:00, not from 'now'.
    start = now.replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    existing = []
    slot = start
    for _ in range(336):  # 7 days * 48 slots/day
        existing.append({
            "start_time": slot,
            "end_time": slot + timedelta(minutes=30)
        })
        slot += timedelta(minutes=30)

    result = rescheduler.reschedule_task(
        task,
        existing,
        now
    )

    assert result is None


def test_reschedule_multiple_tasks(
    rescheduler,
    session,
    student
):

    tasks = [
        _make_task(
            session, student,
            "Task A",
            TaskPriority.HIGH,
            60
        ),
        _make_task(
            session, student,
            "Task B",
            TaskPriority.MEDIUM,
        60
        ),
    ]

    now = datetime.now()

    results = rescheduler.reschedule_multiple_tasks(
        tasks,
        [],
        now
    )

    assert len(results) == 2
