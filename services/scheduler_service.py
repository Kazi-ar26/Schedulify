"""
Schedulify Schedule Service

Responsible for:
- Schedule management
- Rescheduling
- Schedule queries
"""

from datetime import date, datetime
from typing import Optional

from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session

from models.schedule import (
    Schedule,
    ScheduleStatus
)
from models.student import Student
from models.task import Task


class SchedulerService:

    # -------------------------------------------------
    # Time Normalization
    # -------------------------------------------------

    @staticmethod
    def _normalize_time(value):
        """
        Converts datetime values to time values for
        SQLAlchemy Time columns.

        SQLite requires Python datetime.time objects
        for Time columns.
        """

        if isinstance(value, datetime):
            return value.time()

        return value

    # -------------------------------------------------
    # Create
    # -------------------------------------------------

    @staticmethod
    def create_schedule(
        session: Session,
        *,
        student: Student,
        task: Task,
        scheduled_date: datetime,
        start_time,
        end_time,
        generated_by_ai: bool = False
    ) -> Schedule:

        # -------------------------------------------------
        # Prevent duplicate schedules for the same task
        # -------------------------------------------------

        existing_schedule = session.scalar(
            select(Schedule)
            .where(
                Schedule.task_id == task.id
            )
        )

        if existing_schedule is not None:
            return existing_schedule

        # SQLite Time columns require datetime.time
        start_time = SchedulerService._normalize_time(
            start_time
        )

        end_time = SchedulerService._normalize_time(
            end_time
        )

        schedule = Schedule(
            student_id=student.id,
            task_id=task.id,
            scheduled_date=scheduled_date,
            start_time=start_time,
            end_time=end_time,
            generated_by_ai=generated_by_ai
        )

        session.add(schedule)

        try:
            session.commit()
            session.refresh(schedule)
            return schedule

        except Exception:
            session.rollback()
            raise

    # -------------------------------------------------
    # Read
    # -------------------------------------------------

    @staticmethod
    def get_schedule_by_id(
        session: Session,
        schedule_id: int
    ) -> Optional[Schedule]:

        statement = select(Schedule).where(
            Schedule.id == schedule_id
        )

        return session.scalar(statement)

    @staticmethod
    def get_student_schedules(
        session: Session,
        student: Student
    ) -> list[Schedule]:

        statement = (
            select(Schedule)
            .where(
                Schedule.student_id == student.id
            )
            .order_by(
                Schedule.scheduled_date,
                Schedule.start_time
            )
        )

        return list(
            session.scalars(statement).all()
        )

    @staticmethod
    def get_schedules_for_date(
        session: Session,
        student: Student,
        target_date: date
    ) -> list[Schedule]:

        """
        Returns schedules for a specific date.

        Uses SQL filtering instead of loading all records.
        """

        statement = (
            select(Schedule)
            .where(
                Schedule.student_id == student.id
            )
            .where(
                func.date(Schedule.scheduled_date)
                == target_date
            )
            .order_by(Schedule.start_time)
        )

        return list(
            session.scalars(statement).all()
        )

    @staticmethod
    def get_today_schedule(
        session: Session,
        student: Student
    ) -> list[Schedule]:

        return SchedulerService.get_schedules_for_date(
            session,
            student,
            date.today()
        )

    # -------------------------------------------------
    # Update
    # -------------------------------------------------

    @staticmethod
    def update_schedule(
        session: Session,
        schedule: Schedule,
        **changes
    ) -> Schedule:

        for key, value in changes.items():

            if key in ("start_time", "end_time"):
                value = SchedulerService._normalize_time(
                    value
                )

            if hasattr(schedule, key):
                setattr(schedule, key, value)

        session.commit()
        session.refresh(schedule)

        return schedule

    @staticmethod
    def reschedule(
        session: Session,
        schedule: Schedule,
        *,
        scheduled_date: datetime,
        start_time,
        end_time
    ) -> Schedule:

        schedule.scheduled_date = scheduled_date

        schedule.start_time = (
            SchedulerService._normalize_time(
                start_time
            )
        )

        schedule.end_time = (
            SchedulerService._normalize_time(
                end_time
            )
        )

        schedule.status = ScheduleStatus.RESCHEDULED

        session.commit()
        session.refresh(schedule)

        return schedule

    @staticmethod
    def mark_completed(
        session: Session,
        schedule: Schedule
    ) -> Schedule:

        schedule.mark_completed()

        session.commit()
        session.refresh(schedule)

        return schedule

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    @staticmethod
    def delete_schedule(
        session: Session,
        schedule: Schedule
    ) -> None:

        session.delete(schedule)
        session.commit()
