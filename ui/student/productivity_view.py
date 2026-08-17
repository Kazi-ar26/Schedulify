"""
Schedulify Productivity View

Handles:
- Productivity tracking
- Focus session records
- Productivity analytics display

Connects:
UI → AnalyticsController
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QListWidget,
    QMessageBox
)


from controllers.analytics_controller import AnalyticsController



class ProductivityView(QWidget):



    def __init__(
        self,
        analytics_controller: AnalyticsController,
        student
    ):

        super().__init__()

        self.analytics_controller = analytics_controller

        self.student = student

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
            "Productivity Dashboard"
        )



        self.focus_input = QSpinBox()

        self.focus_input.setRange(
            0,
            1440
        )

        self.focus_input.setPrefix(
            "Focus Minutes: "
        )



        self.completed_input = QSpinBox()

        self.completed_input.setRange(
            0,
            100
        )

        self.completed_input.setPrefix(
            "Completed Tasks: "
        )



        self.missed_input = QSpinBox()

        self.missed_input.setRange(
            0,
            100
        )

        self.missed_input.setPrefix(
            "Missed Tasks: "
        )



        self.save_button = QPushButton(
            "Save Productivity"
        )


        self.save_button.clicked.connect(
            self.save_record
        )



        self.analytics_list = QListWidget()



        widgets = [

            self.title,

            self.focus_input,

            self.completed_input,

            self.missed_input,

            self.save_button,

            self.analytics_list

        ]



        for widget in widgets:

            layout.addWidget(
                widget
            )



        self.setLayout(
            layout
        )



    # -------------------------------------------------
    # Save Productivity Record
    # -------------------------------------------------

    def save_record(
        self
    ):


        try:


            record = (

                self.analytics_controller
                .create_productivity_record(

                    self.student,

                    self.focus_input.value(),

                    self.completed_input.value(),

                    self.missed_input.value()

                )

            )


            self.load_analytics()



        except Exception as error:


            QMessageBox.critical(

                self,

                "Productivity Error",

                str(error)

            )

    def load_analytics(self):

        try:

            analytics = (
                self.analytics_controller
                .get_student_analytics(
                    self.student
                )
            )

            summary = analytics["summary"]

            self.analytics_list.clear()

            self.analytics_list.addItem(
                f"Total Tasks: {summary['total_tasks']}"
            )

            self.analytics_list.addItem(
                f"Completed Tasks: {summary['completed_tasks']}"
            )

            self.analytics_list.addItem(
                f"Completion Rate: {summary['completion_rate']}%"
            )

            for record in analytics["productivity"]:

                self.analytics_list.addItem(
                    f"{record.date} | "
                    f"Focus: {record.focus_minutes} min | "
                    f"Completed: {record.completed_tasks} | "
                    f"Missed: {record.missed_tasks}"
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Analytics Error",
                str(error)
            )