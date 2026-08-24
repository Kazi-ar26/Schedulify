"""
Schedulify WellBeing Controller

Handles student wellbeing insights via the backend API.
"""

from api_client.analytics_api import get_student_summary
from api_client.client import APIError


class WellBeingController:

    def __init__(self, session=None):
        self.session = session

    def get_student_insights(self, student_id: int = None) -> dict:
        """Get wellbeing insights derived from analytics."""
        try:
            summary = get_student_summary()
        except APIError:
            summary = {"pending_tasks": 0, "completion_rate": 0}

        pending = summary.get("pending_tasks", 0)

        if pending >= 10:
            workload = "HIGH"
        elif pending >= 5:
            workload = "MEDIUM"
        else:
            workload = "LOW"

        recommendations = []

        if workload == "HIGH":
            recommendations.append(
                "Consider breaking large tasks into smaller sessions."
            )

        rate = summary.get("completion_rate", 0)
        if rate < 50:
            recommendations.append(
                "Try maintaining a more consistent study routine."
            )

        if not recommendations:
            recommendations.append(
                "Your current productivity balance looks stable."
            )

        return {
            "workload_level": workload,
            "consistency_score": round(rate, 2),
            "recommendations": recommendations,
        }
