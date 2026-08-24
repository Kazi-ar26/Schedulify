"""
Schedulify Planner Controller

Handles task planning and schedule generation via the backend API.
"""

from datetime import datetime

from api_client.tasks_api import list_tasks, create_task as api_create_task
from api_client.schedules_api import generate_schedule, list_schedules
from api_client.client import APIError


class PlannerController:

    def __init__(self, session=None):
        self.session = session

    # -------------------------------------------------
    # Task Retrieval
    # -------------------------------------------------

    def get_student_tasks(self, student_id: int = None) -> list[dict]:
        """List all tasks via API."""
        try:
            return list_tasks()
        except APIError:
            return []

    # -------------------------------------------------
    # Create Task
    # -------------------------------------------------

    def create_task(
        self,
        student_id: int = None,
        *,
        title: str,
        description: str = None,
        category: str = None,
        priority=None,
        estimated_duration: int = 60,
        due_date: datetime = None,
    ) -> dict:
        """Create a task via API."""
        priority_str = "medium"
        if priority is not None:
            if hasattr(priority, "value"):
                priority_str = priority.value
            elif isinstance(priority, str):
                priority_str = priority

        due_str = None
        if due_date is not None:
            if isinstance(due_date, datetime):
                due_str = due_date.isoformat()
            else:
                due_str = str(due_date)

        return api_create_task(
            title=title,
            description=description,
            category=category,
            priority=priority_str,
            estimated_duration=estimated_duration,
            due_date=due_str,
        )

    # -------------------------------------------------
    # Generate AI Schedule
    # -------------------------------------------------

    def generate_schedule(self, student_id: int = None) -> list[dict]:
        """Generate an AI schedule via API."""
        return generate_schedule()

    # -------------------------------------------------
    # Get Schedules
    # -------------------------------------------------

    def get_schedules(self, student_id: int = None) -> list[dict]:
        """Get all schedules via API."""
        try:
            return list_schedules()
        except APIError:
            return []
