"""
Schedulify Task Service

Responsible for:
- Task management
- Planner operations
- Task filtering
- Preparing data for the AI Scheduler
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.student import Student
from models.task import (
    Task,
    TaskPriority,
    TaskStatus
)


class TaskService:

    # -------------------------------------------------
    # Create
    # -------------------------------------------------

    @staticmethod
    def create_task(
        session: Session,
        *,
        student: Student,
        title: str,
        description: str | None = None,
        category: str | None = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        estimated_duration: int = 60,
        due_date: datetime | None = None
    ) -> Task:

        task = Task(
            student_id=student.id,
            title=title,
            description=description,
            category=category,
            priority=priority,
            estimated_duration=estimated_duration,
            due_date=due_date
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    # -------------------------------------------------
    # Read
    # -------------------------------------------------

    @staticmethod
    def get_task_by_id(
        session: Session,
        task_id: int
    ) -> Optional[Task]:

        statement = select(Task).where(
            Task.id == task_id
        )

        return session.scalar(statement)

    @staticmethod
    def get_student_tasks(
        session: Session,
        student: Student
    ) -> list[Task]:

        statement = (
            select(Task)
            .where(Task.student_id == student.id)
            .order_by(Task.due_date)
        )

        return list(session.scalars(statement).all())

    @staticmethod
    def get_tasks_by_status(
        session: Session,
        student: Student,
        status: TaskStatus
    ) -> list[Task]:

        statement = (
            select(Task)
            .where(Task.student_id == student.id)
            .where(Task.status == status)
        )

        return list(session.scalars(statement).all())

    @staticmethod
    def get_overdue_tasks(
        session: Session,
        student: Student
    ) -> list[Task]:

        now = datetime.now(timezone.utc)

        statement = (
            select(Task)
            .where(Task.student_id == student.id)
            .where(Task.status != TaskStatus.COMPLETED)
            .where(Task.due_date < now)
        )

        return list(session.scalars(statement).all())

    @staticmethod
    def get_upcoming_tasks(
        session: Session,
        student: Student
    ) -> list[Task]:

        now = datetime.now(timezone.utc)

        statement = (
            select(Task)
            .where(Task.student_id == student.id)
            .where(Task.status == TaskStatus.PENDING)
            .where(Task.due_date >= now)
            .order_by(Task.due_date)
        )

        return list(session.scalars(statement).all())

    # -------------------------------------------------
    # Update
    # -------------------------------------------------

    @staticmethod
    def update_task(
        session: Session,
        task: Task,
        **changes
    ) -> Task:

        for key, value in changes.items():

            if hasattr(task, key):
                setattr(task, key, value)

        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def mark_completed(
        session: Session,
        task: Task
    ) -> Task:

        task.mark_completed()

        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def mark_missed(
        session: Session,
        task: Task
    ) -> Task:

        task.status = TaskStatus.MISSED

        session.commit()
        session.refresh(task)

        return task

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    @staticmethod
    def delete_task(
        session: Session,
        task: Task
    ) -> None:

        session.delete(task)
        session.commit()

    # -------------------------------------------------
    # AI Scheduler
    # -------------------------------------------------

    @staticmethod
    def get_unscheduled_tasks(
        session: Session,
        student: Student
    ) -> list[Task]:
        """
        Returns tasks that are still pending.

        The AI Scheduler uses this method to determine
        which tasks should be placed into the timetable.
        """

        statement = (
            select(Task)
            .where(Task.student_id == student.id)
            .where(Task.status == TaskStatus.PENDING)
            .order_by(
                Task.priority.desc(),
                Task.due_date
            )
        )

        return list(session.scalars(statement).all())