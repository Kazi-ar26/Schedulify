"""
Schedulify Anonymous Reports View

Displays privacy-safe aggregated student insights.
No individual student data is exposed.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
    QPushButton,
)

from PySide6.QtGui import QFont

from controllers.analytics_controller import AnalyticsController


class AnonymousReports(QWidget):

    def __init__(self, analytics_controller: AnalyticsController, user: dict):
        super().__init__()
        self.analytics_controller = analytics_controller
        self.user = user
        self.setup_ui()
        self.load_reports()

    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        title = QLabel("Anonymous Student Reports")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        privacy_note = QLabel(
            "🔒 All data shown here is aggregated and anonymized. "
            "No individual student information is displayed."
        )
        privacy_note.setStyleSheet(
            "color: #9AA2B1; font-size: 13px; padding: 8px 12px; "
            "background: #171B24; border-radius: 8px; border: 1px solid #252B38;"
        )
        privacy_note.setWordWrap(True)
        layout.addWidget(privacy_note)

        # Summary cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        self.card_students = self._create_card("Students", "0")
        self.card_tasks = self._create_card("Tasks Created", "0")
        self.card_completed = self._create_card("Tasks Done", "0")
        self.card_focus = self._create_card("Avg Focus", "0 min")

        for card in [self.card_students, self.card_tasks, self.card_completed, self.card_focus]:
            cards_layout.addWidget(card)

        layout.addLayout(cards_layout)

        # Insight section
        insight_frame = QFrame()
        insight_frame.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 20px;
            }
        """)
        insight_layout = QVBoxLayout(insight_frame)

        insight_title = QLabel("Class Insights")
        insight_title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        insight_layout.addWidget(insight_title)

        self.insight_label = QLabel("Loading...")
        self.insight_label.setStyleSheet("color: #9AA2B1; font-size: 14px; padding: 8px 0;")
        self.insight_label.setWordWrap(True)
        insight_layout.addWidget(self.insight_label)

        layout.addWidget(insight_frame)

        # Refresh
        self.refresh_button = QPushButton("Refresh Report")
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
        self.refresh_button.clicked.connect(self.load_reports)
        layout.addWidget(self.refresh_button)

        layout.addStretch()
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def load_reports(self):
        try:
            data = self.analytics_controller.get_teacher_analytics()
        except Exception:
            return

        stats = data.get("statistics", {})

        students = stats.get("total_students", 0)
        tasks = stats.get("total_tasks", 0)
        completed = stats.get("completed_tasks", 0)
        rate = stats.get("average_completion_rate", 0)
        focus = stats.get("average_focus_minutes", 0)

        self.card_students.findChild(QLabel, "cardValue").setText(str(students))
        self.card_tasks.findChild(QLabel, "cardValue").setText(str(tasks))
        self.card_completed.findChild(QLabel, "cardValue").setText(str(completed))
        self.card_focus.findChild(QLabel, "cardValue").setText(f"{focus:.0f} min")

        if students == 0:
            self.insight_label.setText(
                "No aggregated data available yet.\n"
                "Data will appear once students start using the platform."
            )
        else:
            parts = []
            parts.append(f"📊 {students} students are actively using Schedulify.")
            parts.append(f"📝 {tasks} tasks have been created across the class.")

            if completed > 0:
                parts.append(f"✅ {completed} tasks have been completed ({rate:.1f}% completion rate).")

            if focus > 0:
                parts.append(f"⏱️ Average focus time per session: {focus:.0f} minutes.")

            self.insight_label.setText("\n\n".join(parts))

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
        t = QLabel(title)
        t.setStyleSheet("color: #9AA2B1; font-size: 12px; font-weight: 500;")
        layout.addWidget(t)
        v = QLabel(value)
        v.setObjectName("cardValue")
        v.setStyleSheet("color: white; font-size: 24px; font-weight: 700;")
        layout.addWidget(v)
        return card
