"""
Schedulify Planner View

Handles:
- Student task planning
- AI schedule generation
- Schedule display
- Task creation

Connects:
UI → PlannerController
"""


from datetime import datetime



from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QMessageBox,
    QLineEdit,
    QComboBox,
    QSpinBox
)


from controllers.planner_controller import PlannerController
from models.task import TaskPriority


class PlannerView(QWidget):


    def __init__(
        self,
        planner_controller: PlannerController,
        student
    ):

        super().__init__()


        self.planner_controller = planner_controller

        self.student = student


        self.setup_ui()



    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        self.title = QLabel(
            "Smart Planner"
        )
        self.title.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            """
        )


        # -----------------------------
        # Task Creation
        # -----------------------------

        self.task_input = QLineEdit()

        self.task_input.setPlaceholderText(
            "Enter task name"
        )



        self.duration_label = QLabel(
            "Estimated Duration (minutes)"
        )


        self.duration_input = QSpinBox()

        self.duration_input.setRange(
            15,
            600
        )

        self.duration_input.setValue(
            60
        )

        self.duration_label.setStyleSheet(
            """
            font-size: 14px;
            font-weight: bold;
            """
        )



        self.priority_input = QComboBox()

        self.priority_label = QLabel(
        "Task Priority"
        )

        self.priority_label.setStyleSheet(
            """
            font-size: 14px;
            font-weight: bold;
            """
        )

        self.priority_input.addItems(
            [
                TaskPriority.LOW.value,
                TaskPriority.MEDIUM.value,
                TaskPriority.HIGH.value
            ]
        )



        self.add_task_button = QPushButton(
            "Add Task"
        )


        self.add_task_button.clicked.connect(
            self.create_task
        )



        # -----------------------------
        # AI Scheduler
        # -----------------------------

        self.generate_button = QPushButton(
            "Generate AI Schedule"
        )


        self.generate_button.clicked.connect(
            self.generate_schedule
        )



        self.schedule_list = QListWidget()



        widgets = [

            self.title,

            self.task_input,

            self.duration_label,

            self.duration_input,

            self.priority_label,

            self.priority_input,

            self.add_task_button,

            self.generate_button,

            self.schedule_list

        ]



        for widget in widgets:

            layout.addWidget(
                widget
            )



        self.setLayout(
            layout
        )



    # -------------------------------------------------
    # Create Task
    # -------------------------------------------------

    def create_task(
        self
    ):


        try:


            title = self.task_input.text().strip()



            if not title:


                QMessageBox.warning(

                    self,

                    "Missing Task",

                    "Please enter a task name."

                )

                return



            priority = TaskPriority(

                self.priority_input.currentText()

            )



            self.planner_controller.create_task(

                self.student,

                title=title,

                priority=priority,

                estimated_duration=
                    self.duration_input.value()

            )



            QMessageBox.information(

                self,

                "Success",

                "Task added successfully."

            )



            self.task_input.clear()



        except Exception as error:


            QMessageBox.critical(

                self,

                "Task Error",

                str(error)

            )



    # -------------------------------------------------
    # Generate Schedule
    # -------------------------------------------------

    def generate_schedule(
        self
    ):


        try:


            schedule = (

                self.planner_controller
                .generate_schedule(

                    self.student,

                    datetime.now()

                )

            )


            self.planner_controller.save_schedule(
                self.student,
                schedule
            )


            self.display_schedule(
                schedule
            )



        except Exception as error:


            QMessageBox.critical(

                self,

                "Scheduler Error",

                str(error)

            )



    # -------------------------------------------------
    # Display Schedule
    # -------------------------------------------------

    def display_schedule(
        self,
        schedule
    ):


        self.schedule_list.clear()



        for item in schedule:


            task = item["task"]



            self.schedule_list.addItem(

                f"{task.title} | "
                f"{item['start_time'].strftime('%H:%M')} - "
                f"{item['end_time'].strftime('%H:%M')}"

            )