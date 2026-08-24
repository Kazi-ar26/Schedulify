"""
Schedulify Calendar Controller

Handles calendar operations via the backend API.
"""

from datetime import datetime, timedelta

from api_client.calendar_api import (
    list_events,
    create_event as api_create_event,
)
from api_client.schedules_api import list_schedules
from api_client.client import APIError


class CalendarController:

    def __init__(self, session=None):
        self.session = session

    def get_events(self, student_id: int = None) -> list[dict]:
        """List all calendar events via API."""
        try:
            return list_events()
        except APIError:
            return []

    def get_schedules(self, student_id: int = None) -> list[dict]:
        """List all schedules via API."""
        try:
            return list_schedules()
        except APIError:
            return []

    def get_upcoming_events(self, student_id: int = None) -> list[dict]:
        """Get future calendar events."""
        try:
            events = list_events()
            now = datetime.now().isoformat()
            return [
                e for e in events
                if e.get("start_time", "") > now
            ]
        except APIError:
            return []

    def create_event(
        self,
        student_id: int = None,
        title: str = "",
        description: str = "",
        start_time: datetime = None,
        end_time: datetime = None,
    ) -> dict:
        """Create a calendar event via API."""
        return api_create_event(
            title=title,
            start_time=start_time.isoformat() if start_time else "",
            end_time=end_time.isoformat() if end_time else "",
            description=description,
        )

    def get_future_free_slots(
        self,
        student_id: int = None,
        schedule: dict = None,
    ) -> list[datetime]:
        """Generate future free slots for rescheduling."""
        slots = []
        now = datetime.now()
        for day in range(1, 8):
            future_date = now + timedelta(days=day)
            for hour in range(8, 22):
                slot = future_date.replace(
                    hour=hour, minute=0, second=0, microsecond=0
                )
                slots.append(slot)
        return slots
