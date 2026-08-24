"""
Schedulify Auth Routes

Endpoints:
    POST /api/auth/register  - Create new account
    POST /api/auth/login     - Authenticate and get token
    GET  /api/auth/me        - Get current user profile
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from backend.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
    StudentProfileResponse,
    TeacherProfileResponse,
)
from models.user import User, UserRole
from models.student import Student
from models.teacher import Teacher
from services.settings_service import SettingsService

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new student or teacher account."""

    # Check for duplicate email
    existing = (
        db.query(User)
        .filter(User.email == body.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    # Create user
    user = User(
        email=body.email,
        password_hash=hash_password(body.password),
        first_name=body.first_name,
        last_name=body.last_name,
        role=UserRole(body.role),
        is_active=True,
    )
    db.add(user)
    db.flush()

    # Create role-specific profile
    if body.role == "student":
        profile = Student(
            user_id=user.id,
            school_name=body.school_name,
            grade_level=body.grade_level,
        )
        db.add(profile)
    elif body.role == "teacher":
        profile = Teacher(user_id=user.id)
        db.add(profile)

    # Create default settings
    db.flush()
    settings = SettingsService.create_default_settings(db, user)

    db.commit()
    db.refresh(user)

    # Generate token
    token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate with email and password."""

    user = (
        db.query(User)
        .filter(User.email == body.email)
        .first()
    )

    if user is None or not verify_password(
        body.password, user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated.",
        )

    token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile with role-specific data."""

    result = {
        "user": UserResponse.model_validate(current_user),
        "profile": None,
    }

    if current_user.role == UserRole.STUDENT:
        if current_user.student_profile:
            result["profile"] = StudentProfileResponse.model_validate(
                current_user.student_profile
            )

    elif current_user.role == UserRole.TEACHER:
        if current_user.teacher_profile:
            result["profile"] = TeacherProfileResponse.model_validate(
                current_user.teacher_profile
            )

    return result
