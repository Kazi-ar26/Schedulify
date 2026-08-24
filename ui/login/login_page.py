"""
Schedulify Login Page

Handles:
- User login interface
- Input validation
- Authentication requests via API

Connects:
UI → AuthController → API
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QPixmap

from controllers.auth_controller import AuthController
from ui.login.register_page import RegisterPage


class LoginPage(QWidget):

    login_successful = Signal(dict)

    def __init__(self, auth_controller: AuthController):
        super().__init__()
        self.setWindowTitle("Schedulify — Sign In")
        self.setMinimumSize(480, 600)
        self.auth_controller = auth_controller
        self.registration_page = None
        self.setup_ui()

    def setup_ui(self):
        # Main centered layout
        outer = QVBoxLayout()
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.setContentsMargins(60, 40, 60, 40)

        # Logo / App Name
        logo_label = QLabel("✦ Schedulify")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: #FFC107; margin-bottom: 4px;")
        outer.addWidget(logo_label)

        subtitle = QLabel("Sign in to your account")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #9AA2B1; margin-bottom: 24px;")
        outer.addWidget(subtitle)

        # Card container
        card = QFrame()
        card.setObjectName("loginCard")
        card.setMaximumWidth(380)
        card.setStyleSheet("""
            QFrame#loginCard {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 16px;
                padding: 32px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(32, 32, 32, 32)

        # Email
        email_label = QLabel("Email")
        email_label.setStyleSheet("color: #9AA2B1; font-size: 13px; font-weight: 500;")
        card_layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("you@example.com")
        self.email_input.setMinimumHeight(42)
        self.email_input.setStyleSheet("""
            QLineEdit {
                background: #111318;
                border: 1px solid #303747;
                border-radius: 10px;
                padding: 10px 14px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #FFC107;
            }
        """)
        card_layout.addWidget(self.email_input)

        # Password
        pw_label = QLabel("Password")
        pw_label.setStyleSheet("color: #9AA2B1; font-size: 13px; font-weight: 500;")
        card_layout.addWidget(pw_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(42)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: #111318;
                border: 1px solid #303747;
                border-radius: 10px;
                padding: 10px 14px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #FFC107;
            }
        """)
        card_layout.addWidget(self.password_input)

        card_layout.addSpacing(8)

        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.setMinimumHeight(44)
        self.login_button.setObjectName("primary")
        self.login_button.setStyleSheet("""
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
        self.login_button.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_button)

        card_layout.addSpacing(4)

        # Register link
        register_layout = QHBoxLayout()
        register_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        register_text = QLabel("Don't have an account?")
        register_text.setStyleSheet("color: #9AA2B1; font-size: 13px;")
        register_layout.addWidget(register_text)

        self.register_button = QPushButton("Create Account")
        self.register_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #FFC107;
                border: none;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                color: #FFB300;
            }
        """)
        self.register_button.clicked.connect(self.open_registration)
        register_layout.addWidget(self.register_button)
        card_layout.addLayout(register_layout)

        outer.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(outer)

        # Return to login from registration
        self.login_button.setDefault(True)

    def open_registration(self):
        self.registration_page = RegisterPage(self.auth_controller)
        self.registration_page.registration_successful.connect(
            self.on_registration_success
        )
        self.registration_page.show()

    def on_registration_success(self, user_data: dict):
        """After registration, show message to log in."""
        self.email_input.clear()
        self.password_input.clear()

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(
                self,
                "Login Error",
                "Please enter email and password.",
            )
            return

        self.login_button.setEnabled(False)
        self.login_button.setText("Signing in...")

        try:
            user = self.auth_controller.login(email, password)

            if user:
                self.login_successful.emit(user)
                self.close()
                return

            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid email or password.",
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Connection Error",
                f"Unable to connect to server.\n\n{error}",
            )
        finally:
            self.login_button.setEnabled(True)
            self.login_button.setText("Sign In")
