"""
Schedulify Login Page

Handles:
- User login interface
- Input validation
- Authentication requests

Connects:
UI → AuthController
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)


from PySide6.QtCore import Signal


from controllers.auth_controller import AuthController
from ui.login.register_page import RegisterPage


class LoginPage(QWidget):


    # Emitted after successful login

    login_successful = Signal(object)



    def __init__(
        self,
        auth_controller: AuthController
    ):

        super().__init__()

        self.setWindowTitle("Schedulify Login")


        self.auth_controller = auth_controller
        self.registration_page = None

        self.setup_ui()



    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):


        layout = QVBoxLayout()


        self.title = QLabel(
            "Welcome to Schedulify"
        )


        self.email_input = QLineEdit()

        self.email_input.setPlaceholderText(
            "Email"
        )


        self.password_input = QLineEdit()

        self.password_input.setPlaceholderText(
            "Password"
        )

        self.password_input.setEchoMode(
            QLineEdit.Password
        )



        self.login_button = QPushButton(
            "Login"
        )


        self.login_button.clicked.connect(
            self.handle_login
        )

        self.register_button = QPushButton(
            "Create Account"
        )

        self.register_button.clicked.connect(
            self.open_registration
        )

        layout.addWidget(
            self.register_button
        )



        layout.addWidget(
            self.title
        )


        layout.addWidget(
            self.email_input
        )


        layout.addWidget(
            self.password_input
        )


        layout.addWidget(
            self.login_button
        )


        self.setLayout(
            layout
        )

    def open_registration(self):

        self.registration_page = RegisterPage(
            self.auth_controller
        )

        self.registration_page.show()

    # -------------------------------------------------
    # Login Handling
    # -------------------------------------------------

    def handle_login(
        self
    ):


        email = self.email_input.text().strip()


        password = self.password_input.text()



        if not email or not password:


            QMessageBox.warning(

                self,

                "Login Error",

                "Please enter email and password."

            )


            return



        try:


            user = (

                self.auth_controller
                .login(
                    email,
                    password
                )

            )


            if user:

                self.login_successful.emit(
                    user
                )

                self.close()

                return



            QMessageBox.warning(

                self,

                "Login Failed",

                "Invalid email or password."

            )



        except Exception as error:


            QMessageBox.critical(

                self,

                "Error",

                str(error)

            )