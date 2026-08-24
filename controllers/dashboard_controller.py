"""
Schedulify Dashboard Controller

Handles dashboard data retrieval via the backend API.
"""

from api_client.tasks_api import list_tasks
from api_client.analytics_api import get_student_summary, get_teacher_statistics
from api_client.notifications_api import list_notifications
from api_client.client import APIError


class DashboardController:

    def __init__(self, session=None):
        self.session = session

    # -------------------------------------------------
    # Student Dashboard
    # -------------------------------------------------

    def get_student_dashboard(self, student_id: int) -> dict:
        """
        Get dashboard data for a student.
        student_id is the student profile ID from the API.
        """
        try:
            tasks = list_tasks()
        except APIError:
            tasks = []

        try:
            analytics = get_student_summary()
        except APIError:
            analytics = {
                "total_tasks": 0,
                "completed_tasks": 0,
                "missed_tasks": 0,
                "pending_tasks": 0,
                "completion_rate": 0,
                "total_focus_minutes": 0,
                "average_focus_minutes": 0,
            }

        try:
            notifications = list_notifications()
        except APIError:
            notifications = []

        # Get wellbeing from summary (we can derive it)
        pending = analytics.get("pending_tasks", 0)
        if pending >= 10:
            workload = "HIGH"
        elif pending >= 5:
            workload = "MEDIUM"
        else:
            workload = "LOW"

        return {
            "tasks": tasks,
            "notifications": notifications,
            "analytics": analytics,
            "wellbeing": {
                "workload_level": workload,
                "consistency_score": 0,
                "recommendations": self._generate_recommendations(
                    workload, analytics
                ),
            },
        }

    # -------------------------------------------------
    # Teacher Dashboard
    # -------------------------------------------------

    def get_teacher_dashboard(self) -> dict:
        """Get dashboard data for a teacher."""
        try:
            statistics = get_teacher_statistics()
        except APIError:
            statistics = {
                "total_students": 0,
                "total_tasks": 0,
                "completed_tasks": 0,
                "average_completion_rate": 0,
                "average_focus_minutes": 0,
            }

        try:
            notifications = list_notifications()
        except APIError:
            notifications = []

        return {
            "statistics": statistics,
            "notifications": notifications,
        }

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    @staticmethod
    def _generate_recommendations(workload: str, analytics: dict) -> list[str]:
        recs = []
        if workload == "HIGH":
            recs.append(
                "Consider breaking large tasks into smaller sessions."
            )
        rate = analytics.get("completion_rate", 0)
        if rate < 50:
            recs.append(
                "Try maintaining a more consistent study routine."
            )
        if not recs:
            recs.append(
                "Your current productivity balance looks stable."
            )
        return recs
