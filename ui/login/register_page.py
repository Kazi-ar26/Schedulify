"""
Schedulify Registration Page

Handles:
- New user registration
- Role selection
- School information
- Input validation
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QFrame,
    QScrollArea,
)

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

from controllers.auth_controller import AuthController
from utils.validators import Validator


class RegisterPage(QWidget):

    registration_successful = Signal(dict)

    def __init__(self, auth_controller: AuthController):
        super().__init__()
        self.setWindowTitle("Schedulify — Create Account")
        self.setMinimumSize(500, 700)
        self.auth_controller = auth_controller
        self.setup_ui()

    def setup_ui(self):
        outer = QVBoxLayout()
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.setContentsMargins(50, 30, 50, 30)

        # Title
        title = QLabel("Create Account")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #FFC107; margin-bottom: 4px;")
        outer.addWidget(title)

        subtitle = QLabel("Join Schedulify to manage your academic workflow")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #9AA2B1; margin-bottom: 20px;")
        outer.addWidget(subtitle)

        # Card
        card = QFrame()
        card.setObjectName("registerCard")
        card.setMaximumWidth(400)
        card.setStyleSheet("""
            QFrame#registerCard {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 16px;
                padding: 24px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)
        card_layout.setContentsMargins(28, 28, 28, 28)

        input_style = """
            QLineEdit, QComboBox {
                background: #111318;
                border: 1px solid #303747;
                border-radius: 10px;
                padding: 10px 14px;
                color: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #FFC107;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 12px;
            }
            QComboBox QAbstractItemView {
                background: #171B24;
                color: white;
                border: 1px solid #303747;
                selection-background-color: #FFC107;
                selection-color: #111;
            }
        """

        label_style = "color: #9AA2B1; font-size: 13px; font-weight: 500;"

        # Name row (first + last)
        name_layout = QHBoxLayout()
        name_layout.setSpacing(10)

        for label_text, attr_name in [("First Name", "first_name"), ("Last Name", "last_name")]:
            col = QVBoxLayout()
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            col.addWidget(lbl)
            inp = QLineEdit()
            inp.setPlaceholderText(label_text)
            inp.setMinimumHeight(40)
            inp.setStyleSheet(input_style)
            setattr(self, f"{attr_name}_input", inp)
            col.addWidget(inp)
            name_layout.addLayout(col)

        card_layout.addLayout(name_layout)

        # Email
        lbl = QLabel("Email")
        lbl.setStyleSheet(label_style)
        card_layout.addWidget(lbl)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("you@example.com")
        self.email_input.setMinimumHeight(40)
        self.email_input.setStyleSheet(input_style)
        card_layout.addWidget(self.email_input)

        # Password row
        pw_layout = QHBoxLayout()
        pw_layout.setSpacing(10)
        for label_text, attr_name, placeholder in [
            ("Password", "password_input", "Min 8 chars"),
            ("Confirm", "confirm_input", "Repeat password"),
        ]:
            col = QVBoxLayout()
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            col.addWidget(lbl)
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            inp.setEchoMode(QLineEdit.EchoMode.Password)
            inp.setMinimumHeight(40)
            inp.setStyleSheet(input_style)
            setattr(self, attr_name, inp)
            col.addWidget(inp)
            pw_layout.addLayout(col)

        card_layout.addLayout(pw_layout)

        # Role
        lbl = QLabel("I am a...")
        lbl.setStyleSheet(label_style)
        card_layout.addWidget(lbl)
        self.role_selector = QComboBox()
        self.role_selector.addItems(["Student", "Teacher"])
        self.role_selector.setMinimumHeight(40)
        self.role_selector.setStyleSheet(input_style)
        card_layout.addWidget(self.role_selector)

        # School info (optional)
        lbl = QLabel("School Name (optional)")
        lbl.setStyleSheet(label_style)
        card_layout.addWidget(lbl)
        self.school_input = QLineEdit()
        self.school_input.setPlaceholderText("e.g. Springfield High")
        self.school_input.setMinimumHeight(40)
        self.school_input.setStyleSheet(input_style)
        card_layout.addWidget(self.school_input)

        lbl = QLabel("Grade Level (optional)")
        lbl.setStyleSheet(label_style)
        card_layout.addWidget(lbl)
        self.grade_input = QLineEdit()
        self.grade_input.setPlaceholderText("e.g. 11th Grade")
        self.grade_input.setMinimumHeight(40)
        self.grade_input.setStyleSheet(input_style)
        card_layout.addWidget(self.grade_input)

        card_layout.addSpacing(8)

        # Register button
        self.register_button = QPushButton("Create Account")
        self.register_button.setMinimumHeight(44)
        self.register_button.setStyleSheet("""
            QPushButton {
                background: #FFC107;
                color: #111111;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #FFB300;
            }
            QPushButton:pressed {
                background: #E6AC00;
            }
        """)
        self.register_button.clicked.connect(self.handle_register)
        card_layout.addWidget(self.register_button)

        outer.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(outer)

    def handle_register(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        role = self.role_selector.currentText().lower()
        school = self.school_input.text().strip() or None
        grade = self.grade_input.text().strip() or None

        # Validate
        if not all([first_name, last_name, email, password]):
            QMessageBox.warning(
                self,
                "Registration Error",
                "All required fields must be filled.",
            )
            return

        if not Validator.validate_email(email):
            QMessageBox.warning(
                self,
                "Invalid Email",
                "Please enter a valid email address.",
            )
            return

        if not Validator.validate_password(password):
            QMessageBox.warning(
                self,
                "Weak Password",
                "Password must be at least 8 characters "
                "with uppercase, lowercase, and a number.",
            )
            return

        if password != confirm:
            QMessageBox.warning(
                self,
                "Password Mismatch",
                "Passwords do not match.",
            )
            return

        try:
            if role == "student":
                user = self.auth_controller.register_student(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    school_name=school,
                    grade_level=grade,
                )
            else:
                user = self.auth_controller.register_teacher(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                )

            QMessageBox.information(
                self,
                "Registration Successful",
                "Account created successfully.\n\n"
                "Please sign in with your new account.",
            )

            self.registration_successful.emit(user)
            self.close()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Registration Failed",
                str(error),
            )
