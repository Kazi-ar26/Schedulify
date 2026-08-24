"""
Schedulify Notifications API Service
"""

from api_client.client import get_client


def list_notifications() -> list[dict]:
    """List all notifications."""
    return get_client().get("/api/notifications")


def mark_read(notification_id: int):
    """Mark a notification as read."""
    get_client().post(f"/api/notifications/{notification_id}/read")


def mark_all_read():
    """Mark all notifications as read."""
    get_client().post("/api/notifications/read-all")


def delete_notification(notification_id: int):
    """Delete a notification."""
    get_client().delete(f"/api/notifications/{notification_id}")
