"""
Schedulify Student Dashboard

Displays:
- Student overview with greeting
- Today's tasks
- Summary cards
- Notifications
- Wellbeing indicators

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
    QSpacerItem,
    QSizePolicy,
)

from PySide6.QtGui import QFont

from controllers.dashboard_controller import DashboardController


class StudentDashboard(QWidget):

    def __init__(
        self,
        dashboard_controller: DashboardController,
        user: dict,
    ):
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

        # ---- Greeting ----
        self.greeting = QLabel("Good morning!")
        self.greeting.setObjectName("dashboardTitle")
        self.greeting.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        self.greeting.setStyleSheet("color: white;")
        layout.addWidget(self.greeting)

        subtitle = QLabel("Here's your productivity overview")
        subtitle.setStyleSheet("color: #9AA2B1; font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(subtitle)

        # ---- Summary Cards ----
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        self.card_today = self._create_card("Today's Tasks", "0")
        self.card_completed = self._create_card("Completed", "0")
        self.card_pending = self._create_card("Pending", "0")
        self.card_focus = self._create_card("Focus Time", "0 min")

        for card in [
            self.card_today,
            self.card_completed,
            self.card_pending,
            self.card_focus,
        ]:
            cards_layout.addWidget(card)

        layout.addLayout(cards_layout)

        # ---- Sections Row ----
        sections = QHBoxLayout()
        sections.setSpacing(16)

        # Tasks Section
        tasks_frame = self._create_section("Recent Tasks")
        self.task_list = QListWidget()
        self.task_list.setMinimumHeight(200)
        self.task_list.setMaximumHeight(300)
        tasks_frame.layout().addWidget(self.task_list)
        sections.addWidget(tasks_frame)

        # Notifications Section
        notif_frame = self._create_section("Notifications")
        self.notif_list = QListWidget()
        self.notif_list.setMinimumHeight(200)
        self.notif_list.setMaximumHeight(300)
        notif_frame.layout().addWidget(self.notif_list)
        sections.addWidget(notif_frame)

        layout.addLayout(sections)

        # ---- Wellbeing Section ----
        wellbeing_frame = self._create_section("Wellbeing")
        self.wellbeing_label = QLabel("Loading...")
        self.wellbeing_label.setStyleSheet("color: #9AA2B1; font-size: 14px; padding: 8px;")
        self.wellbeing_label.setWordWrap(True)
        wellbeing_frame.layout().addWidget(self.wellbeing_label)
        layout.addWidget(wellbeing_frame)

        layout.addStretch()

        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def load_dashboard(self):
        try:
            data = self.dashboard_controller.get_student_dashboard(
                self.user.get("id", 0)
            )
        except Exception:
            return

        # Greeting
        first_name = self.user.get("first_name", "")
        if first_name:
            self.greeting.setText(f"Good day, {first_name} 👋")

        # Summary cards
        analytics = data.get("analytics", {})
        tasks = data.get("tasks", [])

        total = analytics.get("total_tasks", 0)
        completed = analytics.get("completed_tasks", 0)
        pending = analytics.get("pending_tasks", total - completed)
        focus = analytics.get("total_focus_minutes", 0)

        self.card_today.findChild(QLabel, "cardValue").setText(str(total))
        self.card_completed.findChild(QLabel, "cardValue").setText(str(completed))
        self.card_pending.findChild(QLabel, "cardValue").setText(str(pending))
        self.card_focus.findChild(QLabel, "cardValue").setText(f"{int(focus)} min")

        # Tasks
        self.task_list.clear()
        if tasks:
            for task in tasks[:10]:
                if isinstance(task, dict):
                    title = task.get("title", "Task")
                    priority = task.get("priority", "")
                    status = task.get("status", "")
                    self.task_list.addItem(
                        f"{'✅ ' if status == 'completed' else '📌 '}"
                        f"{title}  [{priority}]"
                    )
                else:
                    self.task_list.addItem(str(task))
        else:
            self.task_list.addItem("No tasks yet. Create one in the Planner!")

        # Notifications
        self.notif_list.clear()
        notifications = data.get("notifications", [])
        if notifications:
            for n in notifications[:5]:
                if isinstance(n, dict):
                    self.notif_list.addItem(
                        f"🔔 {n.get('title', 'Notification')}"
                    )
                else:
                    self.notif_list.addItem(str(n))
        else:
            self.notif_list.addItem("No new notifications")

        # Wellbeing
        wellbeing = data.get("wellbeing", {})
        if isinstance(wellbeing, dict):
            workload = wellbeing.get("workload_level", "N/A")
            recs = wellbeing.get("recommendations", [])
            recs_text = "\n".join(f"• {r}" for r in recs) if recs else "• All good!"
            self.wellbeing_label.setText(
                f"Workload: {workload}\n\n{recs_text}"
            )

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
            QFrame:hover {
                border: 1px solid #3B4354;
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
