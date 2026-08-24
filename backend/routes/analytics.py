"""
Schedulify Analytics Routes

Endpoints:
    GET  /api/analytics/student        - Student summary
    GET  /api/analytics/productivity   - Student productivity records
    POST /api/analytics/productivity   - Create productivity record
    GET  /api/analytics/teacher        - Teacher class statistics
"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.security import get_current_user
from backend.schemas import (
    ProductivityRecordCreate,
    ProductivityRecordResponse,
    StudentSummary,
    ClassStatistics,
)
from models.user import User, UserRole
from models.student import Student
from models.task import Task, TaskStatus
from models.productivity import ProductivityRecord
from models.analytics import AnalyticsRecord

router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
)


def _get_student(user: User, db: Session) -> Student:
    if user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=403,
            detail="Only students can access student analytics.",
        )
    student = (
        db.query(Student)
        .filter(Student.user_id == user.id)
        .first()
    )
    if student is None:
        raise HTTPException(status_code=404, detail="Student profile not found.")
    return student


@router.get("/student", response_model=StudentSummary)
def get_student_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get aggregated student analytics summary."""
    student = _get_student(current_user, db)

    # Task counts
    total = db.scalar(
        select(func.count(Task.id))
        .where(Task.student_id == student.id)
    ) or 0

    completed = db.scalar(
        select(func.count(Task.id))
        .where(Task.student_id == student.id)
        .where(Task.status == TaskStatus.COMPLETED)
    ) or 0

    missed = db.scalar(
        select(func.count(Task.id))
        .where(Task.student_id == student.id)
        .where(Task.status == TaskStatus.MISSED)
    ) or 0

    pending = db.scalar(
        select(func.count(Task.id))
        .where(Task.student_id == student.id)
        .where(Task.status == TaskStatus.PENDING)
    ) or 0

    # Productivity aggregation
    total_focus = db.scalar(
        select(func.coalesce(func.sum(ProductivityRecord.focus_minutes), 0))
        .where(ProductivityRecord.student_id == student.id)
    ) or 0

    record_count = db.scalar(
        select(func.count(ProductivityRecord.id))
        .where(ProductivityRecord.student_id == student.id)
    ) or 0

    completion_rate = (completed / total * 100) if total > 0 else 0
    avg_focus = (total_focus / record_count) if record_count > 0 else 0

    return StudentSummary(
        total_tasks=total,
        completed_tasks=completed,
        missed_tasks=missed,
        pending_tasks=pending,
        completion_rate=round(completion_rate, 2),
        total_focus_minutes=float(total_focus),
        average_focus_minutes=round(float(avg_focus), 1),
        productivity_records=record_count,
    )


@router.get("/productivity", response_model=list[ProductivityRecordResponse])
def get_productivity_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get student productivity records."""
    student = _get_student(current_user, db)

    records = (
        db.query(ProductivityRecord)
        .filter(ProductivityRecord.student_id == student.id)
        .order_by(ProductivityRecord.date.desc())
        .all()
    )

    return [_record_to_response(r) for r in records]


@router.post(
    "/productivity",
    response_model=ProductivityRecordResponse,
    status_code=201,
)
def create_productivity_record(
    body: ProductivityRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Record a productivity session."""
    student = _get_student(current_user, db)

    record = ProductivityRecord(
        student_id=student.id,
        date=date.today(),
        focus_minutes=body.focus_minutes,
        completed_tasks=body.completed_tasks,
        missed_tasks=body.missed_tasks,
        notes=body.notes,
    )
    record.calculate_score()

    db.add(record)
    db.commit()
    db.refresh(record)

    return _record_to_response(record)


@router.get("/teacher", response_model=ClassStatistics)
def get_teacher_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get aggregated class statistics for teachers."""
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=403,
            detail="Only teachers can access class statistics.",
        )

    total_students = db.scalar(
        select(func.count(Student.id))
    ) or 0

    total_tasks = db.scalar(
        select(func.count(Task.id))
    ) or 0

    completed_tasks = db.scalar(
        select(func.count(Task.id))
        .where(Task.status == TaskStatus.COMPLETED)
    ) or 0

    avg_completion = db.scalar(
        select(func.avg(AnalyticsRecord.completion_rate))
    ) or 0

    avg_focus = db.scalar(
        select(func.avg(ProductivityRecord.focus_minutes))
    ) or 0

    return ClassStatistics(
        total_students=total_students,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        average_completion_rate=round(float(avg_completion), 2),
        average_focus_minutes=round(float(avg_focus), 1),
    )


def _record_to_response(record: ProductivityRecord) -> dict:
    return ProductivityRecordResponse(
        id=record.id,
        student_id=record.student_id,
        date=record.date,
        focus_minutes=record.focus_minutes,
        completed_tasks=record.completed_tasks,
        missed_tasks=record.missed_tasks,
        productivity_score=record.productivity_score,
        notes=record.notes,
        created_at=record.created_at,
    )
