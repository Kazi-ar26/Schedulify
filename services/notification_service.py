"""
Schedulify Notification Service

Responsible for:
- Creating notifications
- Retrieving notifications
- Managing notification status
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.notification import (
    Notification,
    NotificationType,
    NotificationPriority
)

from models.user import User



class NotificationService:


    # -------------------------------------------------
    # Create Notification
    # -------------------------------------------------

    @staticmethod
    def create_notification(
        session: Session,
        *,
        user: User,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.SYSTEM,
        priority: NotificationPriority = NotificationPriority.MEDIUM
    ) -> Notification:


        notification = Notification(

            user_id=user.id,

            title=title,

            message=message,

            notification_type=notification_type,

            priority=priority

        )


        session.add(notification)

        session.commit()

        session.refresh(notification)


        return notification



    # -------------------------------------------------
    # Get Notifications
    # -------------------------------------------------

    @staticmethod
    def get_user_notifications(
        session: Session,
        user: User
    ) -> list[Notification]:


        statement = (

            select(Notification)

            .where(
                Notification.user_id == user.id
            )

            .order_by(
                Notification.created_at.desc()
            )

        )


        return list(
            session.scalars(statement).all()
        )



    @staticmethod
    def get_unread_notifications(
        session: Session,
        user: User
    ) -> list[Notification]:


        statement = (

            select(Notification)

            .where(
                Notification.user_id == user.id
            )

            .where(
                Notification.is_read == False
            )

            .order_by(
                Notification.created_at.desc()
            )

        )


        return list(
            session.scalars(statement).all()
        )



    # -------------------------------------------------
    # Update Status
    # -------------------------------------------------

    @staticmethod
    def mark_as_read(
        session: Session,
        notification: Notification
    ) -> Notification:


        notification.mark_as_read()


        session.commit()

        session.refresh(notification)


        return notification



    @staticmethod
    def mark_all_as_read(
        session: Session,
        user: User
    ) -> None:


        notifications = (
            NotificationService
            .get_unread_notifications(
                session,
                user
            )
        )


        for notification in notifications:

            notification.mark_as_read()


        session.commit()



    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    @staticmethod
    def delete_notification(
        session: Session,
        notification: Notification
    ) -> None:


        session.delete(notification)

        session.commit()



    @staticmethod
    def clear_all_notifications(
        session: Session,
        user: User
    ) -> None:


        notifications = (

            NotificationService
            .get_user_notifications(
                session,
                user
            )

        )


        for notification in notifications:

            session.delete(notification)


        session.commit()