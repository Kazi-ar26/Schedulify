"""
Schedulify Settings Routes

Endpoints:
    GET  /api/settings    - Get user settings
    PUT  /api/settings    - Update user settings
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.security import get_current_user
from backend.schemas import SettingsUpdate, SettingsResponse
from models.user import User
from models.setting import Setting

router = APIRouter(
    prefix="/api/settings",
    tags=["Settings"],
)


@router.get("", response_model=SettingsResponse)
def get_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current user settings, creating defaults if needed."""
    settings = (
        db.query(Setting)
        .filter(Setting.user_id == current_user.id)
        .first()
    )

    if settings is None:
        settings = Setting(
            user_id=current_user.id,
            dark_mode=True,
            notifications_enabled=True,
            email_notifications=False,
            auto_reschedule=True,
            default_study_duration=60,
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return _to_response(settings)


@router.put("", response_model=SettingsResponse)
def update_settings(
    body: SettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user settings."""
    settings = (
        db.query(Setting)
        .filter(Setting.user_id == current_user.id)
        .first()
    )

    if settings is None:
        settings = Setting(user_id=current_user.id)
        db.add(settings)
        db.flush()

    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(settings, key):
            setattr(settings, key, value)

    db.commit()
    db.refresh(settings)

    return _to_response(settings)


def _to_response(s: Setting) -> dict:
    return SettingsResponse(
        id=s.id,
        user_id=s.user_id,
        dark_mode=s.dark_mode,
        notifications_enabled=s.notifications_enabled,
        email_notifications=s.email_notifications,
        auto_reschedule=s.auto_reschedule,
        default_study_duration=s.default_study_duration,
    )
