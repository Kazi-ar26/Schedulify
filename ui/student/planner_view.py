"""
Schedulify Planner View

Handles:
- Student task planning
- AI schedule generation
- Task creation

Connects:
UI → PlannerController → API
"""

from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QMessageBox,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QFrame,
    QScrollArea,
    QDateEdit,
)

from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

from controllers.planner_controller import PlannerView as _


class PlannerView(QWidget):

    def __init__(self, planner_controller, user: dict):
        super().__init__()
        self.planner_controller = planner_controller
        self.user = user
        self.setup_ui()

    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        # Title
        title = QLabel("Smart Planner")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        # Task Creation Card
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 20px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)

        card_title = QLabel("Create New Task")
        card_title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        card_layout.addWidget(card_title)

        input_style = """
            QLineEdit, QSpinBox, QComboBox, QDateEdit {
                background: #111318;
                border: 1px solid #303747;
                border-radius: 10px;
                padding: 10px 14px;
                color: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #FFC107;
            }
            QComboBox::drop-down { border: none; padding-right: 12px; }
            QComboBox QAbstractItemView {
                background: #171B24; color: white;
                border: 1px solid #303747;
                selection-background-color: #FFC107;
                selection-color: #111;
            }
        """
        label_style = "color: #9AA2B1; font-size: 13px; font-weight: 500;"

        # Task name
        lbl = QLabel("Task Name")
        lbl.setStyleSheet(label_style)
        card_layout.addWidget(lbl)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("e.g. Complete Physics Chapter 5")
        self.task_input.setMinimumHeight(40)
        self.task_input.setStyleSheet(input_style)
        card_layout.addWidget(self.task_input)

        # Row: priority + duration + due date
        row = QHBoxLayout()
        row.setSpacing(12)

        # Priority
        col = QVBoxLayout()
        lbl = QLabel("Priority")
        lbl.setStyleSheet(label_style)
        col.addWidget(lbl)
        self.priority_input = QComboBox()
        self.priority_input.addItems(["low", "medium", "high"])
        self.priority_input.setCurrentText("medium")
        self.priority_input.setMinimumHeight(40)
        self.priority_input.setStyleSheet(input_style)
        col.addWidget(self.priority_input)
        row.addLayout(col)

        # Duration
        col = QVBoxLayout()
        lbl = QLabel("Duration (min)")
        lbl.setStyleSheet(label_style)
        col.addWidget(lbl)
        self.duration_input = QSpinBox()
        self.duration_input.setRange(15, 600)
        self.duration_input.setValue(60)
        self.duration_input.setMinimumHeight(40)
        self.duration_input.setStyleSheet(input_style)
        col.addWidget(self.duration_input)
        row.addLayout(col)

        # Due date
        col = QVBoxLayout()
        lbl = QLabel("Due Date")
        lbl.setStyleSheet(label_style)
        col.addWidget(lbl)
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(QDate.currentDate().addDays(7))
        self.due_date_input.setMinimumHeight(40)
        self.due_date_input.setStyleSheet(input_style)
        col.addWidget(self.due_date_input)
        row.addLayout(col)

        card_layout.addLayout(row)

        # Add Task button
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.setMinimumHeight(42)
        self.add_task_button.setStyleSheet("""
            QPushButton {
                background: #FFC107;
                color: #111111;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover { background: #FFB300; }
        """)
        self.add_task_button.clicked.connect(self.create_task)
        card_layout.addWidget(self.add_task_button)

        layout.addWidget(card)

        # AI Schedule Section
        schedule_card = QFrame()
        schedule_card.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 20px;
            }
        """)
        sched_layout = QVBoxLayout(schedule_card)
        sched_layout.setSpacing(12)

        sched_title = QLabel("AI Schedule Generator")
        sched_title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        sched_layout.addWidget(sched_title)

        sched_desc = QLabel("Automatically schedule your pending tasks using AI priority planning.")
        sched_desc.setStyleSheet("color: #9AA2B1; font-size: 13px;")
        sched_layout.addWidget(sched_desc)

        self.generate_button = QPushButton("Generate AI Schedule")
        self.generate_button.setMinimumHeight(42)
        self.generate_button.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover { background: #45a049; }
        """)
        self.generate_button.clicked.connect(self.generate_schedule)
        sched_layout.addWidget(self.generate_button)

        self.schedule_list = QListWidget()
        self.schedule_list.setMinimumHeight(150)
        sched_layout.addWidget(self.schedule_list)

        layout.addWidget(schedule_card)

        # Current Tasks
        tasks_card = QFrame()
        tasks_card.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 20px;
            }
        """)
        tc_layout = QVBoxLayout(tasks_card)
        tc_layout.setSpacing(12)

        tc_title = QLabel("Your Tasks")
        tc_title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        tc_layout.addWidget(tc_title)

        self.task_list = QListWidget()
        self.task_list.setMinimumHeight(200)
        tc_layout.addWidget(self.task_list)

        layout.addWidget(tasks_card)

        layout.addStretch()
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        # Load tasks on init
        self.load_tasks()

    def load_tasks(self):
        """Load existing tasks."""
        try:
            tasks = self.planner_controller.get_student_tasks()
            self.task_list.clear()
            if tasks:
                for task in tasks:
                    if isinstance(task, dict):
                        title = task.get("title", "Task")
                        priority = task.get("priority", "")
                        status = task.get("status", "")
                        due = task.get("due_date", "")
                        icon = "✅" if status == "completed" else "📌"
                        self.task_list.addItem(
                            f"{icon} {title}  [{priority}]  {due[:10] if due else ''}"
                        )
            else:
                self.task_list.addItem("No tasks yet. Create one above!")
        except Exception:
            pass

    def load_dashboard(self):
        self.load_tasks()

    def create_task(self):
        title = self.task_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Missing Task", "Please enter a task name.")
            return

        priority = self.priority_input.currentText()
        duration = self.duration_input.value()
        due_date = self.due_date_input.date().toPython()

        try:
            self.planner_controller.create_task(
                title=title,
                priority=priority,
                estimated_duration=duration,
                due_date=datetime.combine(due_date, datetime.min.time()),
            )

            QMessageBox.information(self, "Success", "Task added successfully!")
            self.task_input.clear()
            self.load_tasks()

        except Exception as error:
            QMessageBox.critical(self, "Task Error", str(error))

    def generate_schedule(self):
        try:
            schedule = self.planner_controller.generate_schedule()

            self.schedule_list.clear()

            if not schedule:
                self.schedule_list.addItem("No pending tasks to schedule.")
                return

            for item in schedule:
                if isinstance(item, dict):
                    task_title = item.get("task_title", "Task")
                    start = item.get("start_time", "")
                    end = item.get("end_time", "")
                    # Format times
                    if "T" in str(start):
                        start_str = str(start).split("T")[1][:5]
                    else:
                        start_str = str(start)[:5]
                    if "T" in str(end):
                        end_str = str(end).split("T")[1][:5]
                    else:
                        end_str = str(end)[:5]

                    self.schedule_list.addItem(
                        f"📅 {task_title}  |  {start_str} — {end_str}"
                    )
                else:
                    self.schedule_list.addItem(str(item))

            QMessageBox.information(
                self,
                "Schedule Generated",
                f"Generated schedule for {len(schedule)} tasks.",
            )

        except Exception as error:
            QMessageBox.critical(self, "Scheduler Error", str(error))
