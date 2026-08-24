"""
Schedulify Analytics API Service

Desktop-side analytics operations via HTTP to the backend.
"""

from api_client.client import get_client


def get_student_summary() -> dict:
    """Get aggregated student analytics."""
    return get_client().get("/api/analytics/student")


def get_productivity_records() -> list[dict]:
    """Get student productivity records."""
    return get_client().get("/api/analytics/productivity")


def create_productivity_record(
    focus_minutes: int,
    completed_tasks: int,
    missed_tasks: int,
    notes: str = None,
) -> dict:
    """Record a productivity session."""
    data = {
        "focus_minutes": focus_minutes,
        "completed_tasks": completed_tasks,
        "missed_tasks": missed_tasks,
    }
    if notes:
        data["notes"] = notes
    return get_client().post("/api/analytics/productivity", data)


def get_teacher_statistics() -> dict:
    """Get class-level statistics for teachers."""
    return get_client().get("/api/analytics/teacher")
