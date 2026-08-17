"""
Schedulify Class Analytics View

Handles:
- Class productivity overview
- Anonymous student analytics
- Performance summaries

Connects:
UI → AnalyticsController
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QMessageBox
)


from controllers.analytics_controller import AnalyticsController



class ClassAnalytics(QWidget):



    def __init__(
        self,
        analytics_controller: AnalyticsController,
        user
    ):

        super().__init__()


        self.analytics_controller = analytics_controller

        self.user = user


        self.setup_ui()


        self.load_analytics()



    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        self.title = QLabel(
            "Class Analytics"
        )



        self.refresh_button = QPushButton(
            "Refresh Analytics"
        )


        self.refresh_button.clicked.connect(
            self.load_analytics
        )



        self.analytics_list = QListWidget()



        widgets = [

            self.title,

            self.analytics_list,

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
    # Load Analytics
    # -------------------------------------------------

    def load_analytics(
        self
    ):


        try:


            analytics = (

                self.analytics_controller
                .get_teacher_analytics(
                    self.user
                )

            )


            self.display_data(
                analytics
            )



        except Exception as error:


            QMessageBox.critical(

                self,

                "Analytics Error",

                str(error)

            )



    # -------------------------------------------------
    # Display Data
    # -------------------------------------------------

    def display_data(
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