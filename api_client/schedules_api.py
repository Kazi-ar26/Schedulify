"""
Schedulify Schedules API Service

Desktop-side schedule operations via HTTP to the backend.
"""

from api_client.client import get_client


def list_schedules() -> list[dict]:
    """List all schedules."""
    return get_client().get("/api/schedules")


def create_schedule(
    task_id: int,
    scheduled_date: str,
    start_time: str,
    end_time: str,
    generated_by_ai: bool = False,
) -> dict:
    """Create a schedule."""
    return get_client().post("/api/schedules", {
        "task_id": task_id,
        "scheduled_date": scheduled_date,
        "start_time": start_time,
        "end_time": end_time,
        "generated_by_ai": generated_by_ai,
    })


def generate_schedule() -> list[dict]:
    """AI-generate a schedule for pending tasks."""
    return get_client().post("/api/schedules/generate")


def update_schedule(schedule_id: int, **changes) -> dict:
    """Update a schedule."""
    data = {k: v for k, v in changes.items() if v is not None}
    return get_client().put(f"/api/schedules/{schedule_id}", data)


def delete_schedule(schedule_id: int):
    """Delete a schedule."""
    get_client().delete(f"/api/schedules/{schedule_id}")


def complete_schedule(schedule_id: int) -> dict:
    """Mark a schedule as completed."""
    return get_client().post(f"/api/schedules/{schedule_id}/complete")
