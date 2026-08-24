"""
Schedulify Wellbeing View

Handles:
- Non-clinical wellbeing indicators
- Productivity balance insights
- AI-generated recommendations
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QMessageBox,
    QFrame,
    QScrollArea,
)

from PySide6.QtGui import QFont

from controllers.wellbeing_controller import WellBeingController


class WellbeingView(QWidget):

    def __init__(self, wellbeing_controller: WellBeingController, user: dict):
        self.wellbeing_controller = wellbeing_controller
        self.user = user
        super().__init__()
        self.setup_ui()
        self.load_insights()

    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        title = QLabel("Wellbeing Insights")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        disclaimer = QLabel(
            "These indicators support productivity awareness "
            "and are not medical assessments."
        )
        disclaimer.setStyleSheet(
            "color: #9AA2B1; font-size: 13px; padding: 8px 12px; "
            "background: #171B24; border-radius: 8px; border: 1px solid #252B38;"
        )
        disclaimer.setWordWrap(True)
        layout.addWidget(disclaimer)

        # Insights section
        insights_frame = QFrame()
        insights_frame.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 20px;
            }
        """)
        if_layout = QVBoxLayout(insights_frame)
        if_layout.setSpacing(12)

        self.workload_label = QLabel("Loading...")
        self.workload_label.setStyleSheet("color: white; font-size: 18px; font-weight: 600;")
        if_layout.addWidget(self.workload_label)

        self.consistency_label = QLabel("")
        self.consistency_label.setStyleSheet("color: #9AA2B1; font-size: 14px;")
        if_layout.addWidget(self.consistency_label)

        layout.addWidget(insights_frame)

        # Recommendations
        rec_frame = QFrame()
        rec_frame.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 16px;
            }
        """)
        rf_layout = QVBoxLayout(rec_frame)

        rec_title = QLabel("💡 Recommendations")
        rec_title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        rf_layout.addWidget(rec_title)

        self.insights_list = QListWidget()
        self.insights_list.setMinimumHeight(150)
        rf_layout.addWidget(self.insights_list)

        layout.addWidget(rec_frame)

        # Refresh
        self.refresh_button = QPushButton("Refresh Insights")
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
        self.refresh_button.clicked.connect(self.load_insights)
        layout.addWidget(self.refresh_button)

        layout.addStretch()
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def load_insights(self):
        try:
            insights = self.wellbeing_controller.get_student_insights()
            if isinstance(insights, dict):
                workload = insights.get("workload_level", "UNKNOWN")
                consistency = insights.get("consistency_score", 0)
                recommendations = insights.get("recommendations", [])

                # Workload indicator
                emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(workload, "⚪")
                self.workload_label.setText(f"{emoji} Workload: {workload}")
                self.consistency_label.setText(
                    f"Study consistency: {consistency}%"
                )

                # Recommendations
                self.insights_list.clear()
                if recommendations:
                    for rec in recommendations:
                        self.insights_list.addItem(f"• {rec}")
                else:
                    self.insights_list.addItem("• All good!")
            else:
                self.workload_label.setText("No data available")

        except Exception as error:
            QMessageBox.critical(self, "Wellbeing Error", str(error))

    def load_dashboard(self):
        self.load_insights()
