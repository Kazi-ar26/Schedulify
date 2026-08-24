"""
Schedulify Tasks API Service

Desktop-side task operations via HTTP to the backend.
"""

from api_client.client import get_client


def list_tasks() -> list[dict]:
    """List all tasks."""
    return get_client().get("/api/tasks")


def create_task(
    title: str,
    description: str = None,
    category: str = None,
    priority: str = "medium",
    estimated_duration: int = 60,
    due_date: str = None,
) -> dict:
    """Create a new task."""
    data = {
        "title": title,
        "priority": priority,
        "estimated_duration": estimated_duration,
    }
    if description:
        data["description"] = description
    if category:
        data["category"] = category
    if due_date:
        data["due_date"] = due_date

    return get_client().post("/api/tasks", data)


def update_task(task_id: int, **changes) -> dict:
    """Update a task."""
    # Filter out None values
    data = {k: v for k, v in changes.items() if v is not None}
    return get_client().put(f"/api/tasks/{task_id}", data)


def delete_task(task_id: int):
    """Delete a task."""
    get_client().delete(f"/api/tasks/{task_id}")


def complete_task(task_id: int) -> dict:
    """Mark a task as completed."""
    return get_client().post(f"/api/tasks/{task_id}/complete")
