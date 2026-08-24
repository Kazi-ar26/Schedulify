"""
Schedulify Notification Routes

Endpoints:
    GET  /api/notifications         - List notifications
    POST /api/notifications/{id}/read - Mark as read
    POST /api/notifications/read-all - Mark all as read
    DELETE /api/notifications/{id}  - Delete notification
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.security import get_current_user
from backend.schemas import NotificationResponse
from models.user import User
from models.notification import Notification

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"],
)


@router.get("", response_model=list[NotificationResponse])
def list_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all notifications for the current user."""
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    return [_to_response(n) for n in notifications]


@router.post("/{notification_id}/read")
def mark_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a single notification as read."""
    from datetime import datetime, timezone

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .first()
    )
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found.")

    notification.is_read = True
    notification.read_at = datetime.now(timezone.utc)
    db.commit()

    return {"status": "ok"}


@router.post("/read-all")
def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark all notifications as read."""
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)

    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False,
    ).update({
        "is_read": True,
        "read_at": now,
    })

    db.commit()
    return {"status": "ok"}


@router.delete("/{notification_id}", status_code=204)
def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a notification."""
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .first()
    )
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found.")

    db.delete(notification)
    db.commit()


def _to_response(n: Notification) -> dict:
    return NotificationResponse(
        id=n.id,
        user_id=n.user_id,
        title=n.title,
        message=n.message,
        notification_type=n.notification_type.value,
        priority=n.priority.value,
        is_read=n.is_read,
        created_at=n.created_at,
    )
