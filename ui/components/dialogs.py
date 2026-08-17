"""
Schedulify Dialog Components

Reusable popup dialogs.

Handles:
- Confirmation dialogs
- Input dialogs
- Information messages
- Task creation dialogs
"""


from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QHBoxLayout
)

from PySide6.QtCore import Signal


class ConfirmationDialog(QDialog):

    confirmed = Signal()

    def __init__(
        self,
        message: str
    ):

        super().__init__()

        self.message = message

        self.setup_ui()

    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):

        self.setWindowTitle(
            "Confirmation"
        )

        self.setMinimumWidth(
            350
        )

        layout = QVBoxLayout()

        self.message_label = QLabel(
            self.message
        )

        self.message_label.setWordWrap(
            True
        )

        buttons_layout = QHBoxLayout()

        self.confirm_button = QPushButton(
            "Confirm"
        )

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.confirm_button.clicked.connect(
            self.handle_confirm
        )

        self.cancel_button.clicked.connect(
            self.reject
        )

        buttons_layout.addWidget(
            self.confirm_button
        )

        buttons_layout.addWidget(
            self.cancel_button
        )

        layout.addWidget(
            self.message_label
        )

        layout.addLayout(
            buttons_layout
        )

        self.setLayout(
            layout
        )

    # -------------------------------------------------
    # Confirm
    # -------------------------------------------------

    def handle_confirm(
        self
    ):

        self.confirmed.emit()

        self.accept()


class TaskDialog(QDialog):

    task_created = Signal(
        dict
    )

    def __init__(
        self
    ):

        super().__init__()

        self.setup_ui()

    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):

        self.setWindowTitle(
            "Create Task"
        )

        self.setMinimumWidth(
            400
        )

        layout = QVBoxLayout()

        # ---------------------------------------------
        # Title
        # ---------------------------------------------

        layout.addWidget(
            QLabel(
                "Task Title"
            )
        )

        self.title_input = QLineEdit()

        self.title_input.setPlaceholderText(
            "Enter task title"
        )

        layout.addWidget(
            self.title_input
        )

        # ---------------------------------------------
        # Description
        # ---------------------------------------------

        layout.addWidget(
            QLabel(
                "Description"
            )
        )

        self.description_input = QTextEdit()

        self.description_input.setPlaceholderText(
            "Enter task description (optional)"
        )

        self.description_input.setMinimumHeight(
            100
        )

        layout.addWidget(
            self.description_input
        )

        # ---------------------------------------------
        # Buttons
        # ---------------------------------------------

        buttons_layout = QHBoxLayout()

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.save_button = QPushButton(
            "Create Task"
        )

        self.cancel_button.clicked.connect(
            self.reject
        )

        self.save_button.clicked.connect(
            self.create_task
        )

        buttons_layout.addWidget(
            self.cancel_button
        )

        buttons_layout.addWidget(
            self.save_button
        )

        layout.addLayout(
            buttons_layout
        )

        self.setLayout(
            layout
        )

        # Focus title field when dialog opens
        self.title_input.setFocus()

    # -------------------------------------------------
    # Create Task
    # -------------------------------------------------

    def create_task(
        self
    ):

        title = self.title_input.text().strip()

        description = (
            self.description_input
            .toPlainText()
            .strip()
        )

        # ---------------------------------------------
        # Validation
        # ---------------------------------------------

        if not title:

            self.title_input.setFocus()

            return

        # ---------------------------------------------
        # Task Data
        # ---------------------------------------------

        data = {

            "title":
                title,

            "description":
                description

        }

        self.task_created.emit(
            data
        )

        self.accept()