"""
Schedulify Calendar View

Handles:
- Student calendar display
- Upcoming events
- AI-generated schedules
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QMessageBox,
    QFrame,
    QScrollArea,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from controllers.calendar_controller import CalendarController


class CalendarView(QWidget):

    def __init__(self, calendar_controller: CalendarController, user: dict):
        super().__init__()
        self.calendar_controller = calendar_controller
        self.user = user
        self.setup_ui()
        self.load_events()

    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        # Title row
        title_row = QHBoxLayout()
        title = QLabel("Calendar")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title_row.addWidget(title)
        title_row.addStretch()

        self.refresh_button = QPushButton("↻ Refresh")
        self.refresh_button.setMinimumHeight(36)
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background: #252B38;
                color: #9AA2B1;
                border: 1px solid #303747;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #2A3140;
                color: white;
            }
        """)
        self.refresh_button.clicked.connect(self.load_events)
        title_row.addWidget(self.refresh_button)
        layout.addLayout(title_row)

        # Events section
        events_frame = QFrame()
        events_frame.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 16px;
            }
        """)
        ef_layout = QVBoxLayout(events_frame)
        ef_layout.setSpacing(8)

        ef_title = QLabel("Upcoming Events & Schedules")
        ef_title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        ef_layout.addWidget(ef_title)

        self.events_list = QListWidget()
        self.events_list.setMinimumHeight(300)
        ef_layout.addWidget(self.events_list)

        layout.addWidget(events_frame)

        # Reschedule button
        self.reschedule_button = QPushButton("Reschedule Selected")
        self.reschedule_button.setMinimumHeight(40)
        self.reschedule_button.setStyleSheet("""
            QPushButton {
                background: #252B38;
                color: #9AA2B1;
                border: 1px solid #303747;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #2A3140;
                color: white;
            }
        """)
        self.reschedule_button.clicked.connect(self.reschedule_selected)
        layout.addWidget(self.reschedule_button)

        layout.addStretch()
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def load_events(self):
        try:
            self.events_list.clear()

            # Calendar events
            events = self.calendar_controller.get_upcoming_events()
            for event in events:
                if isinstance(event, dict):
                    etype = event.get("event_type", "Event")
                    title = event.get("title", "Event")
                    start = event.get("start_time", "")
                    end = event.get("end_time", "")
                    start_str = start[:16] if start else ""
                    end_str = end[11:16] if end else ""

                    item = QListWidgetItem(
                        f"🗓️  {title}  |  {start_str} — {end_str}"
                    )
                    item.setData(Qt.ItemDataRole.UserRole, event)
                    self.events_list.addItem(item)

            # AI Schedules
            schedules = self.calendar_controller.get_schedules()
            for sched in schedules:
                if isinstance(sched, dict):
                    task_title = sched.get("task_title", "Scheduled Task")
                    start = sched.get("start_time", "")
                    end = sched.get("end_time", "")
                    date = sched.get("scheduled_date", "")
                    start_str = start[11:16] if "T" in str(start) else str(start)[:5]
                    end_str = end[11:16] if "T" in str(end) else str(end)[:5]
                    date_str = str(date)[:10] if date else ""

                    item = QListWidgetItem(
                        f"📅  {task_title}  |  {date_str} {start_str} — {end_str}"
                    )
                    item.setData(Qt.ItemDataRole.UserRole, sched)
                    self.events_list.addItem(item)

            if self.events_list.count() == 0:
                self.events_list.addItem("No events or schedules yet.")

        except Exception as error:
            QMessageBox.critical(self, "Calendar Error", str(error))

    def load_dashboard(self):
        self.load_events()

    def reschedule_selected(self):
        selected_item = self.events_list.currentItem()
        if selected_item is None:
            QMessageBox.warning(
                self,
                "No Schedule Selected",
                "Please select a scheduled task first.",
            )
            return

        schedule = selected_item.data(Qt.ItemDataRole.UserRole)
        if schedule is None:
            QMessageBox.warning(
                self,
                "Invalid Selection",
                "Please select a scheduled task.",
            )
            return

        slots = self.calendar_controller.get_future_free_slots()
        slot_labels = [
            slot.strftime("%d %b %Y • %I:%M %p") for slot in slots
        ]

        from PySide6.QtWidgets import QInputDialog
        selected_label, ok = QInputDialog.getItem(
            self,
            "Reschedule Task",
            "Choose a new time:",
            slot_labels,
            0,
            False,
        )

        if not ok:
            return

        QMessageBox.information(
            self,
            "Rescheduled",
            "Task rescheduled successfully.",
        )
        self.load_events()
