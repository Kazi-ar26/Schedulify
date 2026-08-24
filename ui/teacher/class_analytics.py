"""
Schedulify Class Analytics View

Displays aggregated class analytics (no individual student data).
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


class ClassAnalytics(QWidget):

    def __init__(self, analytics_controller: AnalyticsController, user: dict):
        super().__init__()
        self.analytics_controller = analytics_controller
        self.user = user
        self.setup_ui()
        self.load_analytics()

    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        title = QLabel("Class Analytics")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        subtitle = QLabel("Aggregated productivity metrics across all students")
        subtitle.setStyleSheet("color: #9AA2B1; font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(subtitle)

        # Cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        self.card_students = self._create_card("Students", "0")
        self.card_tasks = self._create_card("Total Tasks", "0")
        self.card_completed = self._create_card("Tasks Completed", "0")
        self.card_focus = self._create_card("Avg Focus", "0 min")

        for card in [self.card_students, self.card_tasks, self.card_completed, self.card_focus]:
            cards_layout.addWidget(card)

        layout.addLayout(cards_layout)

        # Completion rate bar
        rate_frame = QFrame()
        rate_frame.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 20px;
            }
        """)
        rate_layout = QVBoxLayout(rate_frame)
        rate_title = QLabel("Overall Completion Rate")
        rate_title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        rate_layout.addWidget(rate_title)

        self.rate_label = QLabel("0%")
        self.rate_label.setStyleSheet("color: #FFC107; font-size: 32px; font-weight: 700;")
        rate_layout.addWidget(self.rate_label)

        self.rate_desc = QLabel("Calculating...")
        self.rate_desc.setStyleSheet("color: #9AA2B1; font-size: 13px;")
        rate_layout.addWidget(self.rate_desc)

        layout.addWidget(rate_frame)

        # Refresh
        self.refresh_button = QPushButton("Refresh Analytics")
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
        self.refresh_button.clicked.connect(self.load_analytics)
        layout.addWidget(self.refresh_button)

        layout.addStretch()
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def load_analytics(self):
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

        self.rate_label.setText(f"{rate:.1f}%")

        if rate >= 75:
            self.rate_desc.setText("🟢 Strong — students are on track")
        elif rate >= 50:
            self.rate_desc.setText("🟡 Moderate — room for improvement")
        elif rate > 0:
            self.rate_desc.setText("🔴 Low — students may need support")
        else:
            self.rate_desc.setText("No data available yet")

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
