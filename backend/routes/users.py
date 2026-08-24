"""
Schedulify User Routes

Endpoints:
    GET  /api/users/me      - Get current user
    PUT  /api/users/me      - Update profile
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.security import get_current_user
from backend.schemas import UserResponse
from models.user import User

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    """Get current user profile."""
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
def update_profile(
    first_name: str = None,
    last_name: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user profile."""
    if first_name:
        current_user.first_name = first_name
    if last_name:
        current_user.last_name = last_name

    db.commit()
    db.refresh(current_user)

    return UserResponse.model_validate(current_user)
