"""
Schedulify Wellbeing Service

Responsible for:
- Productivity balance indicators
- Workload analysis
- Study consistency insights

This is NOT a medical system.
"""


from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models.task import Task, TaskStatus
from models.student import Student
from models.productivity import ProductivityRecord



class WellbeingService:



    # -------------------------------------------------
    # Workload Analysis
    # -------------------------------------------------

    @staticmethod
    def calculate_workload_level(
        session: Session,
        student: Student
    ) -> str:


        statement = (

            select(
                func.count(Task.id)
            )

            .where(
                Task.student_id == student.id
            )

            .where(
                Task.status != TaskStatus.COMPLETED
            )

        )


        pending_tasks = session.scalar(
            statement
        ) or 0



        if pending_tasks >= 10:

            return "HIGH"



        if pending_tasks >= 5:

            return "MEDIUM"



        return "LOW"



    # -------------------------------------------------
    # Productivity Consistency
    # -------------------------------------------------

    @staticmethod
    def get_consistency_score(
        session: Session,
        student: Student
    ) -> float:


        records = (

            session.scalars(

                select(ProductivityRecord)

                .where(
                    ProductivityRecord.student_id
                    == student.id
                )

            )

            .all()

        )


        if not records:

            return 0.0



        active_days = len(

            [

                record

                for record in records

                if record.focus_minutes > 0

            ]

        )


        return round(

            (active_days / len(records))
            * 100,

            2

        )



    # -------------------------------------------------
    # Recommendations
    # -------------------------------------------------

    @staticmethod
    def generate_recommendations(
        session: Session,
        student: Student
    ) -> list[str]:


        recommendations = []


        workload = (

            WellbeingService
            .calculate_workload_level(
                session,
                student
            )

        )


        consistency = (

            WellbeingService
            .get_consistency_score(
                session,
                student
            )

        )



        if workload == "HIGH":

            recommendations.append(

                "Consider breaking large tasks into smaller sessions."

            )



        if consistency < 50:

            recommendations.append(

                "Try maintaining a more consistent study routine."

            )



        if not recommendations:

            recommendations.append(

                "Your current productivity balance looks stable."

            )



        return recommendations
    def generate_student_insights(
        self,
        session,
        student
    ):

        workload = self.calculate_workload_level(
            session,
            student
        )

        consistency = self.get_consistency_score(
            session,
            student
        )

        recommendations = self.generate_recommendations(
            session,
            student
        )

        return {
            "workload_level": workload,
            "consistency_score": consistency,
            "recommendations": recommendations
        }