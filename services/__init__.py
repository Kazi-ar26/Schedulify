"""
Schedulify Services Package

Contains the business logic layer.

Services communicate between:
- Controllers
- Database models
- External APIs

They should never directly depend on the UI layer.
"""

__all__ = [
    "AuthService",
    "UserService",
    "TaskService",
    "ScheduleService",
    "CalendarService",
    "NotificationService",
    "AnalyticsService",
    "AISchedulerService",
    "WellbeingService",
]