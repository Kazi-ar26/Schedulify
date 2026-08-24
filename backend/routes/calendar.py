"""
Schedulify Calendar Routes

Endpoints:
    GET  /api/calendar       - List events
    POST /api/calendar       - Create event
    DELETE /api/calendar/{id} - Delete event
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.security import get_current_user
from backend.schemas import CalendarEventCreate, CalendarEventResponse
from models.user import User, UserRole
from models.student import Student
from models.calendar_event import CalendarEvent, EventType

router = APIRouter(
    prefix="/api/calendar",
    tags=["Calendar"],
)


def _get_student(user: User, db: Session) -> Student:
    if user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can manage calendar.",
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


@router.get("", response_model=list[CalendarEventResponse])
def list_events(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all calendar events for the current student."""
    student = _get_student(current_user, db)

    events = (
        db.query(CalendarEvent)
        .filter(CalendarEvent.student_id == student.id)
        .order_by(CalendarEvent.start_time)
        .all()
    )

    return [_event_to_response(e) for e in events]


@router.post("", response_model=CalendarEventResponse, status_code=201)
def create_event(
    body: CalendarEventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new calendar event."""
    student = _get_student(current_user, db)

    event = CalendarEvent(
        student_id=student.id,
        title=body.title,
        description=body.description,
        event_type=EventType(body.event_type),
        start_time=body.start_time,
        end_time=body.end_time,
        location=body.location,
        reminder_enabled=body.reminder_enabled,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return _event_to_response(event)


@router.delete("/{event_id}", status_code=204)
def delete_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a calendar event."""
    student = _get_student(current_user, db)

    event = (
        db.query(CalendarEvent)
        .filter(
            CalendarEvent.id == event_id,
            CalendarEvent.student_id == student.id,
        )
        .first()
    )
    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found.",
        )

    db.delete(event)
    db.commit()


def _event_to_response(event: CalendarEvent) -> dict:
    return CalendarEventResponse(
        id=event.id,
        student_id=event.student_id,
        title=event.title,
        description=event.description,
        event_type=event.event_type.value,
        start_time=event.start_time,
        end_time=event.end_time,
        location=event.location,
        reminder_enabled=event.reminder_enabled,
        created_at=event.created_at,
    )
