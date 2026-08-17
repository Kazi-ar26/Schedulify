"""
Schedulify Anonymous Reports View

Handles:
- Privacy-safe teacher reports
- Aggregated student insights
- Anonymous analytics display

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



class AnonymousReports(QWidget):



    def __init__(
        self,
        analytics_controller: AnalyticsController,
        user
    ):

        super().__init__()


        self.analytics_controller = analytics_controller

        self.user = user


        self.setup_ui()


        self.load_reports()



    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        self.title = QLabel(
            "Anonymous Student Reports"
        )


        self.description = QLabel(

            "Reports contain aggregated insights "
            "to protect student privacy."

        )



        self.refresh_button = QPushButton(
            "Generate Report"
        )


        self.refresh_button.clicked.connect(
            self.load_reports
        )



        self.report_list = QListWidget()



        widgets = [

            self.title,

            self.description,

            self.report_list,

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
    # Load Reports
    # -------------------------------------------------

    def load_reports(
        self
    ):


        try:


            reports = (

                self.analytics_controller
                .get_teacher_analytics(
                    self.user
                )

            )


            self.display_reports(
                reports
            )



        except Exception as error:


            QMessageBox.critical(

                self,

                "Report Error",

                str(error)

            )



    # -------------------------------------------------
    # Display Reports
    # -------------------------------------------------

    def display_reports(
        self,
        reports
    ):


        self.report_list.clear()



        if isinstance(
            reports,
            dict
        ):


            for key, value in reports.items():

                self.report_list.addItem(

                    f"{key}: {value}"

                )


        else:


            self.report_list.addItem(

                str(reports)

            )