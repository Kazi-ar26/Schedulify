"""
Schedulify Teacher Dashboard

Displays:
- Class overview
- Aggregated statistics
- Notifications

Connects:
UI → DashboardController → API
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QFrame,
    QScrollArea,
    QPushButton,
)

from PySide6.QtGui import QFont

from controllers.dashboard_controller import DashboardController


class TeacherDashboard(QWidget):

    def __init__(self, dashboard_controller: DashboardController, user: dict):
        super().__init__()
        self.dashboard_controller = dashboard_controller
        self.user = user
        self.setup_ui()
        self.load_dashboard()

    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        # Greeting
        first = self.user.get("first_name", "")
        greeting = QLabel(f"Welcome, {first}!" if first else "Teacher Dashboard")
        greeting.setObjectName("dashboardTitle")
        greeting.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        greeting.setStyleSheet("color: white;")
        layout.addWidget(greeting)

        subtitle = QLabel("Here's your class overview")
        subtitle.setStyleSheet("color: #9AA2B1; font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(subtitle)

        # Summary cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        self.card_students = self._create_card("Total Students", "0")
        self.card_tasks = self._create_card("Total Tasks", "0")
        self.card_completed = self._create_card("Completed", "0")
        self.card_rate = self._create_card("Completion Rate", "0%")

        for card in [self.card_students, self.card_tasks, self.card_completed, self.card_rate]:
            cards_layout.addWidget(card)

        layout.addLayout(cards_layout)

        # Info section
        info_frame = self._create_section("Class Information")
        self.info_label = QLabel(
            "Aggregated, anonymous analytics from all students.\n"
            "No individual student data is shown here."
        )
        self.info_label.setStyleSheet("color: #9AA2B1; font-size: 14px; padding: 8px;")
        self.info_label.setWordWrap(True)
        info_frame.layout().addWidget(self.info_label)
        layout.addWidget(info_frame)

        # Notifications
        notif_frame = self._create_section("Notifications")
        self.notif_list = QListWidget()
        self.notif_list.setMinimumHeight(150)
        self.notif_list.setMaximumHeight(250)
        notif_frame.layout().addWidget(self.notif_list)
        layout.addWidget(notif_frame)

        # Refresh
        self.refresh_button = QPushButton("Refresh Dashboard")
        self.refresh_button.setMinimumHeight(40)
        self.refresh_button.setStyleSheet("""
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
        self.refresh_button.clicked.connect(self.load_dashboard)
        layout.addWidget(self.refresh_button)

        layout.addStretch()

        scroll.setWidget(content)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def load_dashboard(self):
        try:
            data = self.dashboard_controller.get_teacher_dashboard()
        except Exception:
            return

        stats = data.get("statistics", {})

        students = stats.get("total_students", 0)
        tasks = stats.get("total_tasks", 0)
        completed = stats.get("completed_tasks", 0)
        rate = stats.get("average_completion_rate", 0)

        self.card_students.findChild(QLabel, "cardValue").setText(str(students))
        self.card_tasks.findChild(QLabel, "cardValue").setText(str(tasks))
        self.card_completed.findChild(QLabel, "cardValue").setText(str(completed))
        self.card_rate.findChild(QLabel, "cardValue").setText(f"{rate}%")

        # Notifications
        self.notif_list.clear()
        notifications = data.get("notifications", [])
        if notifications:
            for n in notifications[:10]:
                if isinstance(n, dict):
                    self.notif_list.addItem(
                        f"🔔 {n.get('title', 'Notification')}"
                    )
        else:
            self.notif_list.addItem("No notifications")

    @staticmethod
    def _create_card(title: str, value: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 16px;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setSpacing(6)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #9AA2B1; font-size: 12px; font-weight: 500;")
        layout.addWidget(title_lbl)
        value_lbl = QLabel(value)
        value_lbl.setObjectName("cardValue")
        value_lbl.setStyleSheet("color: white; font-size: 24px; font-weight: 700;")
        layout.addWidget(value_lbl)
        return card

    @staticmethod
    def _create_section(title: str) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 16px;
            }
        """)
        layout = QVBoxLayout(frame)
        layout.setSpacing(8)
        lbl = QLabel(title)
        lbl.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        layout.addWidget(lbl)
        return frame
