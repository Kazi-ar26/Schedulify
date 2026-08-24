"""
Schedulify Productivity View

Handles:
- Productivity tracking
- Focus session records
- Productivity analytics display
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QListWidget,
    QMessageBox,
    QFrame,
    QScrollArea,
)

from PySide6.QtGui import QFont

from controllers.analytics_controller import AnalyticsController


class ProductivityView(QWidget):

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

        title = QLabel("Productivity Dashboard")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        # Summary cards
        self.summary_frame = QFrame()
        self.summary_frame.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 20px;
            }
        """)
        sum_layout = QVBoxLayout(self.summary_frame)
        sum_title = QLabel("Summary")
        sum_title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        sum_layout.addWidget(sum_title)

        self.summary_label = QLabel("Loading...")
        self.summary_label.setStyleSheet("color: #9AA2B1; font-size: 14px;")
        self.summary_label.setWordWrap(True)
        sum_layout.addWidget(self.summary_label)

        layout.addWidget(self.summary_frame)

        # Record Productivity
        record_frame = QFrame()
        record_frame.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 20px;
            }
        """)
        rec_layout = QVBoxLayout(record_frame)
        rec_layout.setSpacing(12)

        rec_title = QLabel("Record Session")
        rec_title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        rec_layout.addWidget(rec_title)

        input_style = """
            QSpinBox {
                background: #111318;
                border: 1px solid #303747;
                border-radius: 10px;
                padding: 10px 14px;
                color: white;
                font-size: 14px;
                min-height: 20px;
            }
            QSpinBox:focus { border: 2px solid #FFC107; }
        """
        label_style = "color: #9AA2B1; font-size: 13px; font-weight: 500;"

        row = QHBoxLayout()
        row.setSpacing(12)

        for label_text, attr_name, prefix in [
            ("Focus Minutes", "focus_input", "Minutes: "),
            ("Completed", "completed_input", "Tasks: "),
            ("Missed", "missed_input", "Tasks: "),
        ]:
            col = QVBoxLayout()
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            col.addWidget(lbl)
            spin = QSpinBox()
            spin.setRange(0, 1440 if "Focus" in label_text else 100)
            spin.setPrefix(prefix)
            spin.setMinimumHeight(40)
            spin.setStyleSheet(input_style)
            setattr(self, attr_name, spin)
            col.addWidget(spin)
            row.addLayout(col)

        rec_layout.addLayout(row)

        self.save_button = QPushButton("Save Record")
        self.save_button.setMinimumHeight(42)
        self.save_button.setStyleSheet("""
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
        self.save_button.clicked.connect(self.save_record)
        rec_layout.addWidget(self.save_button)

        layout.addWidget(record_frame)

        # History
        history_frame = QFrame()
        history_frame.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 16px;
            }
        """)
        hf_layout = QVBoxLayout(history_frame)
        hf_title = QLabel("Session History")
        hf_title.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        hf_layout.addWidget(hf_title)

        self.analytics_list = QListWidget()
        self.analytics_list.setMinimumHeight(200)
        hf_layout.addWidget(self.analytics_list)

        layout.addWidget(history_frame)

        layout.addStretch()
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def save_record(self):
        try:
            self.analytics_controller.create_productivity_record(
                focus_minutes=self.focus_input.value(),
                completed_tasks=self.completed_input.value(),
                missed_tasks=self.missed_input.value(),
            )
            self.load_analytics()
            QMessageBox.information(self, "Saved", "Productivity record saved.")
        except Exception as error:
            QMessageBox.critical(self, "Error", str(error))

    def load_analytics(self):
        try:
            analytics = self.analytics_controller.get_student_analytics()
            summary = analytics.get("summary", {})

            total = summary.get("total_tasks", 0)
            completed = summary.get("completed_tasks", 0)
            rate = summary.get("completion_rate", 0)
            focus = summary.get("total_focus_minutes", 0)

            self.summary_label.setText(
                f"📊 Total Tasks: {total}\n"
                f"✅ Completed: {completed}\n"
                f"📈 Completion Rate: {rate}%\n"
                f"⏱️ Total Focus: {int(focus)} min"
            )

            self.analytics_list.clear()
            records = analytics.get("productivity", [])
            if records:
                for record in records[:20]:
                    if isinstance(record, dict):
                        date = record.get("date", "")
                        focus_min = record.get("focus_minutes", 0)
                        done = record.get("completed_tasks", 0)
                        missed = record.get("missed_tasks", 0)
                        self.analytics_list.addItem(
                            f"📅 {date}  |  Focus: {focus_min} min  |  "
                            f"Done: {done}  |  Missed: {missed}"
                        )
            else:
                self.analytics_list.addItem("No records yet. Start tracking!")

        except Exception as error:
            QMessageBox.critical(self, "Analytics Error", str(error))

    def load_dashboard(self):
        self.load_analytics()
