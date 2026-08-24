"""
Schedulify Calendar API Service

Desktop-side calendar operations via HTTP to the backend.
"""

from api_client.client import get_client


def list_events() -> list[dict]:
    """List all calendar events."""
    return get_client().get("/api/calendar")


def create_event(
    title: str,
    start_time: str,
    end_time: str,
    description: str = None,
    event_type: str = "personal",
    location: str = None,
) -> dict:
    """Create a calendar event."""
    data = {
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "event_type": event_type,
    }
    if description:
        data["description"] = description
    if location:
        data["location"] = location
    return get_client().post("/api/calendar", data)


def delete_event(event_id: int):
    """Delete a calendar event."""
    get_client().delete(f"/api/calendar/{event_id}")
