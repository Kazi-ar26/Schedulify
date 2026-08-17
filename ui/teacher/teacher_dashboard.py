"""
Schedulify Teacher Dashboard

Handles:
- Teacher overview
- Class analytics summary
- Anonymous insights
- Notifications

Connects:
UI → DashboardController
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QMessageBox
)


from controllers.dashboard_controller import DashboardController



class TeacherDashboard(QWidget):



    def __init__(
        self,
        dashboard_controller: DashboardController,
        user
    ):

        super().__init__()


        self.dashboard_controller = dashboard_controller

        self.user = user


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
            "Teacher Dashboard"
        )


        self.refresh_button = QPushButton(
            "Refresh Dashboard"
        )


        self.refresh_button.clicked.connect(
            self.load_dashboard
        )



        self.analytics_list = QListWidget()



        self.notifications_list = QListWidget()



        widgets = [

            self.title,

            QLabel(
                "Anonymous Class Analytics"
            ),

            self.analytics_list,

            QLabel(
                "Notifications"
            ),

            self.notifications_list,

            self.refresh_button

        ]



        for widget in widgets:

            layout.addWidget(
                widget
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


        try:


            data = (

                self.dashboard_controller
                .get_teacher_dashboard(
                    self.user
                )

            )


            self.display_analytics(

                data.get(
                    "analytics",
                    {}
                )

            )


            self.display_notifications(

                data.get(
                    "notifications",
                    []
                )

            )



        except Exception as error:


            QMessageBox.critical(

                self,

                "Dashboard Error",

                str(error)

            )



    # -------------------------------------------------
    # Display Analytics
    # -------------------------------------------------

    def display_analytics(
        self,
        analytics
    ):


        self.analytics_list.clear()



        if isinstance(
            analytics,
            dict
        ):


            for key, value in analytics.items():

                self.analytics_list.addItem(

                    f"{key}: {value}"

                )



        else:


            self.analytics_list.addItem(

                str(analytics)

            )



    # -------------------------------------------------
    # Display Notifications
    # -------------------------------------------------

    def display_notifications(
        self,
        notifications
    ):


        self.notifications_list.clear()



        for notification in notifications:


            self.notifications_list.addItem(

                notification.title

            )