"""
Schedulify Schedule Routes

Endpoints:
    GET  /api/schedules           - List student's schedules
    POST /api/schedules           - Create a schedule
    PUT  /api/schedules/{id}      - Update a schedule
    DELETE /api/schedules/{id}    - Delete a schedule
    POST /api/schedules/generate  - AI generate schedule
    POST /api/schedules/{id}/complete - Mark complete
    POST /api/schedules/{id}/reschedule - Reschedule
"""

from datetime import datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.security import get_current_user
from backend.schemas import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse,
    ScheduleWithTask,
)
from models.user import User, UserRole
from models.student import Student
from models.task import Task, TaskStatus
from models.schedule import Schedule, ScheduleStatus
from ai_engine.smart_scheduler import SmartScheduler
from ai_engine.rescheduler import Rescheduler

router = APIRouter(
    prefix="/api/schedules",
    tags=["Schedules"],
)


def _get_student(user: User, db: Session) -> Student:
    if user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can manage schedules.",
        )
    student = (
        db.query(Student)
        .filter(Student.user_id == user.id)
        .first()
    )
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found.",
        )
    return student


def _normalize_time(value):
    if isinstance(value, datetime):
        return value.time()
    return value


def _schedule_to_response(schedule: Schedule) -> dict:
    return ScheduleResponse(
        id=schedule.id,
        student_id=schedule.student_id,
        task_id=schedule.task_id,
        scheduled_date=schedule.scheduled_date,
        start_time=str(schedule.start_time),
        end_time=str(schedule.end_time),
        generated_by_ai=schedule.generated_by_ai,
        status=schedule.status.value,
        created_at=schedule.created_at,
    )


def _schedule_with_task(schedule: Schedule) -> dict:
    task_title = schedule.task.title if schedule.task else "Scheduled Task"
    task_priority = (
        schedule.task.priority.value if schedule.task else "medium"
    )
    return ScheduleWithTask(
        id=schedule.id,
        student_id=schedule.student_id,
        task_id=schedule.task_id,
        scheduled_date=schedule.scheduled_date,
        start_time=str(schedule.start_time),
        end_time=str(schedule.end_time),
        generated_by_ai=schedule.generated_by_ai,
        status=schedule.status.value,
        created_at=schedule.created_at,
        task_title=task_title,
        task_priority=task_priority,
    )


@router.get("", response_model=list[ScheduleWithTask])
def list_schedules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all schedules for the current student."""
    student = _get_student(current_user, db)

    schedules = (
        db.query(Schedule)
        .filter(Schedule.student_id == student.id)
        .order_by(Schedule.scheduled_date, Schedule.start_time)
        .all()
    )

    return [_schedule_with_task(s) for s in schedules]


@router.post("", response_model=ScheduleResponse, status_code=201)
def create_schedule(
    body: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a manual schedule."""
    student = _get_student(current_user, db)

    # Check task exists and belongs to student
    task = (
        db.query(Task)
        .filter(
            Task.id == body.task_id,
            Task.student_id == student.id,
        )
        .first()
    )
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    # Check for existing schedule for this task
    existing = (
        db.query(Schedule)
        .filter(Schedule.task_id == body.task_id)
        .first()
    )
    if existing:
        return _schedule_to_response(existing)

    # Parse time strings
    start_parts = body.start_time.split(":")
    end_parts = body.end_time.split(":")

    schedule = Schedule(
        student_id=student.id,
        task_id=body.task_id,
        scheduled_date=body.scheduled_date,
        start_time=time(
            int(start_parts[0]),
            int(start_parts[1]) if len(start_parts) > 1 else 0,
        ),
        end_time=time(
            int(end_parts[0]),
            int(end_parts[1]) if len(end_parts) > 1 else 0,
        ),
        generated_by_ai=body.generated_by_ai,
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    return _schedule_to_response(schedule)


@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(
    schedule_id: int,
    body: ScheduleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a schedule."""
    student = _get_student(current_user, db)

    schedule = (
        db.query(Schedule)
        .filter(
            Schedule.id == schedule_id,
            Schedule.student_id == student.id,
        )
        .first()
    )
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found.")

    if body.scheduled_date is not None:
        schedule.scheduled_date = body.scheduled_date
    if body.start_time is not None:
        parts = body.start_time.split(":")
        schedule.start_time = time(
            int(parts[0]),
            int(parts[1]) if len(parts) > 1 else 0,
        )
    if body.end_time is not None:
        parts = body.end_time.split(":")
        schedule.end_time = time(
            int(parts[0]),
            int(parts[1]) if len(parts) > 1 else 0,
        )
    if body.status is not None:
        schedule.status = ScheduleStatus(body.status)

    db.commit()
    db.refresh(schedule)

    return _schedule_to_response(schedule)


@router.delete("/{schedule_id}", status_code=204)
def delete_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a schedule."""
    student = _get_student(current_user, db)

    schedule = (
        db.query(Schedule)
        .filter(
            Schedule.id == schedule_id,
            Schedule.student_id == student.id,
        )
        .first()
    )
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found.")

    db.delete(schedule)
    db.commit()


@router.post("/generate", response_model=list[dict])
def generate_schedule(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """AI-generate a schedule for pending tasks."""
    student = _get_student(current_user, db)

    # Get unscheduled pending tasks
    tasks = (
        db.query(Task)
        .filter(
            Task.student_id == student.id,
            Task.status == TaskStatus.PENDING,
        )
        .order_by(Task.priority.desc(), Task.due_date)
        .all()
    )

    if not tasks:
        return []

    scheduler = SmartScheduler()
    now = datetime.now()
    plan = scheduler.generate_schedule(tasks, now)

    # Save schedules to database
    created = []
    for item in plan:
        # Check for existing schedule
        existing = (
            db.query(Schedule)
            .filter(Schedule.task_id == item["task"].id)
            .first()
        )
        if existing:
            created.append({
                "task_id": item["task"].id,
                "task_title": item["task"].title,
                "start_time": item["start_time"].isoformat(),
                "end_time": item["end_time"].isoformat(),
            })
            continue

        schedule = Schedule(
            student_id=student.id,
            task_id=item["task"].id,
            scheduled_date=item["start_time"],
            start_time=item["start_time"].time(),
            end_time=item["end_time"].time(),
            generated_by_ai=True,
        )
        db.add(schedule)

        created.append({
            "task_id": item["task"].id,
            "task_title": item["task"].title,
            "start_time": item["start_time"].isoformat(),
            "end_time": item["end_time"].isoformat(),
        })

    db.commit()

    return created


@router.post("/{schedule_id}/complete", response_model=ScheduleResponse)
def complete_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a schedule as completed."""
    student = _get_student(current_user, db)

    schedule = (
        db.query(Schedule)
        .filter(
            Schedule.id == schedule_id,
            Schedule.student_id == student.id,
        )
        .first()
    )
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found.")

    schedule.status = ScheduleStatus.COMPLETED
    db.commit()
    db.refresh(schedule)

    return _schedule_to_response(schedule)
