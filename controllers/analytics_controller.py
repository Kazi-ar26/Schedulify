"""
Schedulify Analytics Controller

Handles:
- Student productivity analytics
- Teacher anonymous analytics
- Analytics dashboard data preparation

Connects:
UI → Controller → AnalyticsService
"""


from sqlalchemy.orm import Session


from models.student import Student
from models.user import User


from services.analytics_service import AnalyticsService



class AnalyticsController:



    def __init__(
        self,
        session: Session
    ):

        self.session = session

        self.analytics_service = AnalyticsService()



    # -------------------------------------------------
    # Student Analytics
    # -------------------------------------------------

    def get_student_analytics(
        self,
        student: Student
    ) -> dict:


        productivity = (

            self.analytics_service
            .get_student_productivity(
                self.session,
                student
            )

        )


        summary = (

            self.analytics_service
            .generate_student_summary(
                self.session,
                student
            )

        )


        return {

            "summary": summary,

            "productivity": productivity

        }



    # -------------------------------------------------
    # Create Productivity Analytics
    # -------------------------------------------------

    def create_productivity_record(
        self,
        student: Student,
        focus_minutes: int,
        completed_tasks: int,
        missed_tasks: int,
        notes: str | None = None
    ):


        return (

            self.analytics_service
            .create_productivity_record(
                self.session,

                student=student,

                focus_minutes=focus_minutes,

                completed_tasks=completed_tasks,

                missed_tasks=missed_tasks,

                notes=notes

            )

        )



    # -------------------------------------------------
    # Teacher Analytics
    # -------------------------------------------------

    def get_teacher_analytics(
        self,
        user: User
    ) -> dict:


        statistics = (

            self.analytics_service
            .get_anonymous_class_statistics(
                self.session
            )

        )


        return {

            "statistics": statistics

        }



    # -------------------------------------------------
    # Chart Formatting
    # -------------------------------------------------

    @staticmethod
    def prepare_chart_data(
        records
    ) -> dict:


        labels = []

        values = []



        for record in records:

            labels.append(

                str(record.date)

            )


            values.append(

                record.focus_minutes

            )



        return {

            "labels": labels,

            "values": values

        }