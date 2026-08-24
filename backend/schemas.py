"""
Schedulify Backend Pydantic Schemas

Request/response models for all API endpoints.
"""

from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# -------------------------------------------------
# Auth Schemas
# -------------------------------------------------

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    role: str = Field(pattern=r"^(student|teacher)$")
    school_name: Optional[str] = None
    grade_level: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------------------------------
# Student / Teacher Profile Schemas
# -------------------------------------------------

class StudentProfileResponse(BaseModel):
    id: int
    user_id: int
    school_name: Optional[str] = None
    grade_level: Optional[str] = None
    academic_year: Optional[str] = None
    timezone: str = "UTC"

    class Config:
        from_attributes = True


class TeacherProfileResponse(BaseModel):
    id: int
    user_id: int
    school_name: Optional[str] = None
    department: Optional[str] = None
    subject: Optional[str] = None

    class Config:
        from_attributes = True


# -------------------------------------------------
# Task Schemas
# -------------------------------------------------

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    priority: str = Field(default="medium", pattern=r"^(low|medium|high)$")
    estimated_duration: int = Field(default=60, ge=15, le=600)
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    estimated_duration: Optional[int] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    student_id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    priority: str
    estimated_duration: int
    due_date: Optional[datetime] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# -------------------------------------------------
# Schedule Schemas
# -------------------------------------------------

class ScheduleCreate(BaseModel):
    task_id: int
    scheduled_date: datetime
    start_time: str  # HH:MM format
    end_time: str    # HH:MM format
    generated_by_ai: bool = False


class ScheduleUpdate(BaseModel):
    scheduled_date: Optional[datetime] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status: Optional[str] = None


class ScheduleResponse(BaseModel):
    id: int
    student_id: int
    task_id: int
    scheduled_date: datetime
    start_time: str
    end_time: str
    generated_by_ai: bool
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ScheduleWithTask(ScheduleResponse):
    task_title: Optional[str] = None
    task_priority: Optional[str] = None


# -------------------------------------------------
# Calendar Event Schemas
# -------------------------------------------------

class CalendarEventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    event_type: str = Field(default="personal")
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    reminder_enabled: bool = True


class CalendarEventResponse(BaseModel):
    id: int
    student_id: int
    title: str
    description: Optional[str] = None
    event_type: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    reminder_enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------------------------------
# Analytics Schemas
# -------------------------------------------------

class ProductivityRecordCreate(BaseModel):
    focus_minutes: int = Field(ge=0, le=1440)
    completed_tasks: int = Field(ge=0, le=100)
    missed_tasks: int = Field(ge=0, le=100)
    notes: Optional[str] = None


class ProductivityRecordResponse(BaseModel):
    id: int
    student_id: int
    date: date
    focus_minutes: int
    completed_tasks: int
    missed_tasks: int
    productivity_score: float
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StudentSummary(BaseModel):
    total_tasks: int
    completed_tasks: int
    missed_tasks: int
    pending_tasks: int
    completion_rate: float
    total_focus_minutes: float
    average_focus_minutes: float
    productivity_records: int


class ClassStatistics(BaseModel):
    total_students: int
    total_tasks: int
    completed_tasks: int
    average_completion_rate: float
    average_focus_minutes: float


# -------------------------------------------------
# Notification Schemas
# -------------------------------------------------

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    priority: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------------------------------
# Settings Schemas
# -------------------------------------------------

class SettingsUpdate(BaseModel):
    dark_mode: Optional[bool] = None
    notifications_enabled: Optional[bool] = None
    email_notifications: Optional[bool] = None
    auto_reschedule: Optional[bool] = None
    default_study_duration: Optional[int] = None


class SettingsResponse(BaseModel):
    id: int
    user_id: int
    dark_mode: bool
    notifications_enabled: bool
    email_notifications: bool
    auto_reschedule: bool
    default_study_duration: int

    class Config:
        from_attributes = True


# -------------------------------------------------
# Wellbeing Schemas
# -------------------------------------------------

class WellbeingInsights(BaseModel):
    workload_level: str
    consistency_score: float
    recommendations: list[str]


# -------------------------------------------------
# Teacher Dashboard Schemas
# -------------------------------------------------

class TeacherDashboard(BaseModel):
    statistics: ClassStatistics
    notifications: list[NotificationResponse]


# -------------------------------------------------
# Reschedule Schemas
# -------------------------------------------------

class RescheduleRequest(BaseModel):
    schedule_id: int
    new_start_time: datetime
