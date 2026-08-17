"""
Schedulify Card Components

Reusable dashboard cards.

Used for:
- Tasks
- Analytics
- Productivity metrics
- Summary information
"""


from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel
)


from PySide6.QtCore import Qt



class BaseCard(QFrame):



    def __init__(
        self,
        title: str,
        value: str = ""
    ):

        super().__init__()


        self.title_text = title

        self.value_text = value


        self.setup_ui()



    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):


        self.setFrameShape(
            QFrame.StyledPanel
        )


        layout = QVBoxLayout()



        self.title_label = QLabel(
            self.title_text
        )


        self.title_label.setAlignment(
            Qt.AlignCenter
        )



        self.value_label = QLabel(
            self.value_text
        )


        self.value_label.setAlignment(
            Qt.AlignCenter
        )



        layout.addWidget(
            self.title_label
        )


        layout.addWidget(
            self.value_label
        )


        self.setLayout(
            layout
        )



    # -------------------------------------------------
    # Update Value
    # -------------------------------------------------

    def update_value(
        self,
        value: str
    ):


        self.value_label.setText(
            value
        )



class TaskCard(BaseCard):



    def __init__(
        self,
        task
    ):


        super().__init__(

            title="Task",

            value=task.title

        )


        self.task = task



class AnalyticsCard(BaseCard):



    def __init__(
        self,
        title: str,
        metric
    ):


        super().__init__(

            title,

            str(metric)

        )



class ProductivityCard(BaseCard):



    def __init__(
        self,
        focus_minutes: int
    ):


        super().__init__(

            "Focus Time",

            f"{focus_minutes} minutes"

        )