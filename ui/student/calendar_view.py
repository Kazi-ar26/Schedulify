"""
Schedulify Calendar View

Handles:

- Student calendar display
- Upcoming events
- AI-generated schedules
- Schedule overview

Connects:
UI → CalendarController
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QMessageBox,
    QInputDialog
)

from PySide6.QtCore import Qt

from controllers.calendar_controller import CalendarController
from models.user import UserRole


class CalendarView(QWidget):

    def __init__(
        self,
        calendar_controller: CalendarController,
        student
    ):

        super().__init__()

        self.calendar_controller = calendar_controller

        self.student = student

        self.setup_ui()

        self.load_events()


    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):

        layout = QVBoxLayout()

        self.title = QLabel(
            "Calendar"
        )

        self.refresh_button = QPushButton(
            "Refresh"
        )

        self.refresh_button.clicked.connect(
            self.load_events
        )

        self.events_list = QListWidget()

        self.reschedule_button = QPushButton(
        "Reschedule Selected"
        )

        self.reschedule_button.clicked.connect(
            self.reschedule_selected
    )

        widgets = [

            self.title,

            self.refresh_button,

            self.events_list,

            self.reschedule_button

        ]

        for widget in widgets:

            layout.addWidget(
                widget
            )

        self.setLayout(
            layout
        )


    # -------------------------------------------------
    # Load Events + AI Schedules
    # -------------------------------------------------

    def load_events(self):

        try:

            events = self.calendar_controller.get_upcoming_events(
                self.student
            )

            schedules = self.calendar_controller.get_schedules(
                self.student
            )

            self.events_list.clear()

            # Calendar events
            for event in events:

                item = QListWidgetItem(
                    f"SCHEDULE | "
                    f"{task_title} | "
                    f"{schedule.scheduled_date.strftime('%d %b %Y')} "
                    f"{schedule.start_time.strftime('%H:%M')} - "
                    f"{schedule.end_time.strftime('%H:%M')}"
                )

                item.setData(
                    Qt.ItemDataRole.UserRole,
                    schedule
                )

                self.events_list.addItem(item)
            # AI schedules
            for schedule in schedules:

                task_title = (
                    schedule.task.title
                    if schedule.task
                    else "Scheduled Task"
                )

                item = QListWidgetItem(
                    f"SCHEDULE | "
                    f"{task_title} | "
                    f"{schedule.scheduled_date.strftime('%d %b %Y')} "
                    f"{schedule.start_time.strftime('%H:%M')} - "
                    f"{schedule.end_time.strftime('%H:%M')}"
                )

                item.setData(Qt.UserRole, schedule)

                self.events_list.addItem(item)

        except Exception as error:

            QMessageBox.critical(
                self,
                "Calendar Error",
                str(error)
            )

    def reschedule_selected(self):

        selected_item = self.events_list.currentItem()

        if selected_item is None:

            QMessageBox.warning(
                self,
                "No Schedule Selected",
                "Please select a scheduled task first."
            )

            return

        schedule = selected_item.data(
            Qt.ItemDataRole.UserRole
        )

        if schedule is None:

            QMessageBox.warning(
                self,
                "Invalid Selection",
                "Please select a scheduled task."
            )

            return

        slots = self.calendar_controller.get_future_free_slots(
            self.student,
            schedule
        )

        slot_labels = [
            slot.strftime("%d %b %Y • %I:%M %p")
            for slot in slots
        ]

        selected_label, ok = QInputDialog.getItem(
            self,
            "Reschedule Task",
            "Choose a new time:",
            slot_labels,
            0,
            False
        )

        if not ok:
            return

        selected_index = slot_labels.index(
            selected_label
        )

        selected_slot = slots[selected_index]

        try:

            self.calendar_controller.reschedule_schedule(
                schedule,
                selected_slot
            )

            self.load_events()

            QMessageBox.information(
                self,
                "Rescheduled",
                "Task rescheduled successfully."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Reschedule Failed",
                str(error)
            )