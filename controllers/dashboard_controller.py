"""
Schedulify Dashboard Controller

Handles dashboard data retrieval for:
- Students
- Teachers

Connects:
UI → Controller → Services
"""


from sqlalchemy.orm import Session


from models.user import User, UserRole
from models.student import Student


from services.task_service import TaskService
from services.analytics_service import AnalyticsService
from services.notification_service import NotificationService
from services.wellbeing_service import WellbeingService



class DashboardController:


    def __init__(
        self,
        session: Session
    ):

        self.session = session

        self.task_service = TaskService()

        self.analytics_service = AnalyticsService()

        self.notification_service = NotificationService()

        self.wellbeing_service = WellbeingService()



    # -------------------------------------------------
    # Student Dashboard
    # -------------------------------------------------

    def get_student_dashboard(
        self,
        student: Student
    ) -> dict:


        tasks = (

            self.task_service
            .get_student_tasks(
                self.session,
                student
            )

        )


        notifications = (

            self.notification_service
            .get_user_notifications(
                self.session,
                student.user
            )

        )


        analytics = (

            self.analytics_service
            .generate_student_summary(
                self.session,
                student
            )

        )


        wellbeing = (

            self.wellbeing_service
            .generate_recommendations(
                self.session,
                student
            )

        )


        return {

            "tasks": tasks,

            "notifications": notifications,

            "analytics": analytics,

            "wellbeing": wellbeing

        }



    # -------------------------------------------------
    # Teacher Dashboard
    # -------------------------------------------------

    def get_teacher_dashboard(
        self,
        user: User
    ) -> dict:


        analytics = (

            self.analytics_service
            .get_anonymous_class_statistics(
                self.session
            )

        )


        notifications = (

            self.notification_service
            .get_user_notifications(
                self.session,
                user
            )

        )


        return {

            "analytics": analytics,

            "notifications": notifications

        }



    # -------------------------------------------------
    # Universal Dashboard Router
    # -------------------------------------------------

    def get_dashboard(
        self,
        user: User
    ) -> dict:


        if user.role == UserRole.STUDENT:

            return self.get_student_dashboard(
                user.student_profile
            )


        if user.role == UserRole.TEACHER:

            return self.get_teacher_dashboard(
                user
            )


        return {}