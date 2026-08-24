"""
Schedulify Analytics Controller

Handles analytics via the backend API.
"""

from api_client.analytics_api import (
    get_student_summary,
    get_productivity_records,
    create_productivity_record as api_create_record,
    get_teacher_statistics,
)
from api_client.client import APIError


class AnalyticsController:

    def __init__(self, session=None):
        self.session = session

    def get_student_analytics(self, student_id: int = None) -> dict:
        """Get student analytics via API."""
        try:
            summary = get_student_summary()
        except APIError:
            summary = {
                "total_tasks": 0,
                "completed_tasks": 0,
                "completion_rate": 0,
            }

        try:
            productivity = get_productivity_records()
        except APIError:
            productivity = []

        return {
            "summary": summary,
            "productivity": productivity,
        }

    def create_productivity_record(
        self,
        student_id: int = None,
        focus_minutes: int = 0,
        completed_tasks: int = 0,
        missed_tasks: int = 0,
        notes: str = None,
    ) -> dict:
        """Record productivity via API."""
        return api_create_record(
            focus_minutes=focus_minutes,
            completed_tasks=completed_tasks,
            missed_tasks=missed_tasks,
            notes=notes,
        )

    def get_teacher_analytics(self) -> dict:
        """Get teacher analytics via API."""
        try:
            return {"statistics": get_teacher_statistics()}
        except APIError:
            return {
                "statistics": {
                    "total_students": 0,
                    "total_tasks": 0,
                    "completed_tasks": 0,
                    "average_completion_rate": 0,
                    "average_focus_minutes": 0,
                }
            }
