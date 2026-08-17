"""
Schedulify Wellbeing View

Handles:
- Non-clinical wellbeing indicators
- Productivity balance insights
- AI-generated recommendations

Connects:
UI → WellbeingService
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QMessageBox
)


from controllers.wellbeing_controller import WellBeingController



class WellbeingView(QWidget):



    def __init__(
        self,
        wellbeing_controller: WellBeingController,
        student
    ):

        self.wellbeing_controller = wellbeing_controller
        self.student = student

        super().__init__()

        self.setup_ui()


        self.load_insights()



    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        self.title = QLabel(
            "Wellbeing Insights"
        )


        self.description = QLabel(

            "These indicators are designed "
            "to support productivity awareness "
            "and are not medical assessments."

        )



        self.refresh_button = QPushButton(
            "Refresh Insights"
        )


        self.refresh_button.clicked.connect(
            self.load_insights
        )



        self.insights_list = QListWidget()



        widgets = [

            self.title,

            self.description,

            self.refresh_button,

            self.insights_list

        ]



        for widget in widgets:

            layout.addWidget(
                widget
            )



        self.setLayout(
            layout
        )



    # -------------------------------------------------
    # Load Wellbeing Data
    # -------------------------------------------------

    def load_insights(
        self
    ):


        try:


            insights = (
                self.wellbeing_controller
                .get_student_insights(
                    self.student
                )
            )


            self.display_insights(
                insights
            )



        except Exception as error:


            QMessageBox.critical(

                self,

                "Wellbeing Error",

                str(error)

            )



    # -------------------------------------------------
    # Display Insights
    # -------------------------------------------------

    def display_insights(
        self,
        insights
    ):

        self.insights_list.clear()

        if not isinstance(insights, dict):
            return

        workload = insights.get(
            "workload_level",
            "UNKNOWN"
        )

        consistency = insights.get(
            "consistency_score",
            0
        )

        recommendations = insights.get(
            "recommendations",
            []
        )

        self.insights_list.addItem(
            f"🌱 Workload Level: {workload}"
        )

        self.insights_list.addItem(
            f"📚 Study Consistency: {consistency}%"
        )

        self.insights_list.addItem(
            ""
        )

        self.insights_list.addItem(
            "💡 Recommendations"
        )

        for recommendation in recommendations:

            self.insights_list.addItem(
                f"• {recommendation}"
            )