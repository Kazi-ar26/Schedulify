"""
Schedulify Student Dashboard

Displays:
- Student overview
- Today's tasks
- Productivity summary
- Notifications
- Wellbeing indicators

Connects:
UI → DashboardController
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QFrame
)


from controllers.dashboard_controller import DashboardController



class StudentDashboard(QWidget):



    def __init__(
        self,
        dashboard_controller: DashboardController,
        student
    ):

        super().__init__()


        self.dashboard_controller = dashboard_controller

        self.student = student


        self.setup_ui()


        self.load_dashboard()



    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        self.title = QLabel(
            "Student Dashboard"
        )


        self.title.setObjectName(
            "dashboardTitle"
        )



        self.task_section = QListWidget()



        self.notification_section = QListWidget()



        self.analytics_label = QLabel(
            "Productivity: Loading..."
        )



        self.wellbeing_label = QLabel(
            "Wellbeing: Loading..."
        )



        sections = [

            self.title,

            QLabel("Today's Tasks"),

            self.task_section,

            QLabel("Notifications"),

            self.notification_section,

            self.analytics_label,

            self.wellbeing_label

        ]



        for section in sections:

            layout.addWidget(
                section
            )



        self.setLayout(
            layout
        )



    # -------------------------------------------------
    # Load Dashboard Data
    # -------------------------------------------------

    def load_dashboard(
        self
    ):


        data = (

            self.dashboard_controller
            .get_student_dashboard(
                self.student
            )

        )



        self.load_tasks(

            data.get(
                "tasks",
                []
            )

        )


        self.load_notifications(

            data.get(
                "notifications",
                []
            )

        )



        self.analytics_label.setText(

            f"Productivity: "
            f"{data.get('analytics', {})}"

        )



        self.wellbeing_label.setText(

            f"Wellbeing: "
            f"{data.get('wellbeing', {})}"

        )



    # -------------------------------------------------
    # Task Display
    # -------------------------------------------------

    def load_tasks(
        self,
        tasks
    ):


        self.task_section.clear()



        for task in tasks:


            self.task_section.addItem(

                f"{task.title} | "
                f"{task.priority.value}"

            )



    # -------------------------------------------------
    # Notification Display
    # -------------------------------------------------

    def load_notifications(
        self,
        notifications
    ):


        self.notification_section.clear()



        for notification in notifications:


            self.notification_section.addItem(

                notification.title

            )
