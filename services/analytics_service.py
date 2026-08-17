"""
Schedulify Analytics Service

Responsible for:
- Productivity analytics
- Dashboard statistics
- Anonymous teacher analytics
"""

from datetime import date

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.student import Student
from models.task import Task, TaskStatus
from models.productivity import ProductivityRecord
from models.analytics import AnalyticsRecord



class AnalyticsService:


    # -------------------------------------------------
    # Productivity Records
    # -------------------------------------------------

    @staticmethod
    def create_productivity_record(
        session: Session,
        *,
        student: Student,
        focus_minutes: int,
        completed_tasks: int,
        missed_tasks: int,
        notes: str | None = None
    ) -> ProductivityRecord:


        record = ProductivityRecord(

            student_id=student.id,

            date=date.today(),

            focus_minutes=focus_minutes,

            completed_tasks=completed_tasks,

            missed_tasks=missed_tasks,

            notes=notes

        )


        record.calculate_score()


        session.add(record)

        session.commit()

        session.refresh(record)


        return record



    # -------------------------------------------------
    # Student Analytics
    # -------------------------------------------------

    @staticmethod
    def get_student_productivity(
        session: Session,
        student: Student
    ) -> list[ProductivityRecord]:


        statement = (

            select(ProductivityRecord)

            .where(
                ProductivityRecord.student_id == student.id
            )

            .order_by(
                ProductivityRecord.date.desc()
            )

        )


        return list(
            session.scalars(statement).all()
        )



    @staticmethod
    def generate_student_summary(
        session: Session,
        student: Student
    ) -> dict:

        # Get total number of tasks
        total = session.scalar(
            select(func.count(Task.id))
            .where(
                Task.student_id == student.id
            )
        ) or 0

        # Get latest productivity record
        latest_record = session.scalar(
            select(ProductivityRecord)
            .where(
                ProductivityRecord.student_id == student.id
            )
            .order_by(
                ProductivityRecord.date.desc()
            )
        )

        if latest_record:

            completed = latest_record.completed_tasks

            missed = latest_record.missed_tasks

        else:

            completed = 0
            missed = 0

        completion_rate = (
            (completed / total) * 100
            if total > 0
            else 0
        )

        return {

            "total_tasks": total,

            "completed_tasks": completed,

            "missed_tasks": missed,

            "completion_rate": round(
                completion_rate,
                2
            )

        }



    # -------------------------------------------------
    # Analytics Records
    # -------------------------------------------------

    @staticmethod
    def create_analytics_record(
        session: Session,
        *,
        student: Student,
        completion_rate: float,
        average_focus_time: float,
        workload_score: float
    ) -> AnalyticsRecord:


        record = AnalyticsRecord(

            student_id=student.id,

            record_date=date.today(),

            completion_rate=completion_rate,

            average_focus_time=average_focus_time,

            workload_score=workload_score

        )


        record.update_productivity_score()


        session.add(record)

        session.commit()

        session.refresh(record)


        return record



    # -------------------------------------------------
    # Teacher Anonymous Analytics
    # -------------------------------------------------

    @staticmethod
    def get_anonymous_class_statistics(
        session: Session
    ) -> dict:


        total_students = (

            session.scalar(

                select(
                    func.count(Student.id)
                )

            )

        )


        average_completion = (

            session.scalar(

                select(
                    func.avg(
                        AnalyticsRecord.completion_rate
                    )
                )

            )

        )


        return {

            "total_students": total_students or 0,

            "average_completion_rate":

                round(
                    average_completion or 0,
                    2
                )

        }