"""
Schedulify Registration Page

Handles:
- New user registration
- Role selection
- Input validation

Connects:
UI → AuthController
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox
)


from PySide6.QtCore import Signal


from controllers.auth_controller import AuthController



class RegisterPage(QWidget):


    registration_successful = Signal(object)



    def __init__(
        self,
        auth_controller: AuthController
    ):

        super().__init__()


        self.auth_controller = auth_controller


        self.setup_ui()



    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        self.title = QLabel(
            "Create Schedulify Account"
        )



        self.first_name_input = QLineEdit()

        self.first_name_input.setPlaceholderText(
            "First Name"
        )



        self.last_name_input = QLineEdit()

        self.last_name_input.setPlaceholderText(
            "Last Name"
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



        self.role_selector = QComboBox()


        self.role_selector.addItems(

            [

                "Student",

                "Teacher"

            ]

        )



        self.register_button = QPushButton(
            "Register"
        )


        self.register_button.clicked.connect(
            self.handle_register
        )



        widgets = [

            self.title,

            self.first_name_input,

            self.last_name_input,

            self.email_input,

            self.password_input,

            self.role_selector,

            self.register_button

        ]



        for widget in widgets:

            layout.addWidget(
                widget
            )



        self.setLayout(
            layout
        )



    # -------------------------------------------------
    # Registration Handling
    # -------------------------------------------------

    def handle_register(
        self
    ):


        first_name = (

            self.first_name_input
            .text()
            .strip()

        )


        last_name = (

            self.last_name_input
            .text()
            .strip()

        )


        email = (

            self.email_input
            .text()
            .strip()

        )


        password = (

            self.password_input
            .text()

        )


        role = (

            self.role_selector
            .currentText()

        )



        if not all(

            [

                first_name,

                last_name,

                email,

                password

            ]

        ):


            QMessageBox.warning(

                self,

                "Registration Error",

                "All fields are required."

            )


            return



        try:


            if role == "Student":


                user = (

                    self.auth_controller
                    .register_student(

                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,

                    )

                )


            else:


                user = (

                    self.auth_controller
                    .register_teacher(

                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                    )

                )



            QMessageBox.information(
                self,
                "Registration Successful",
                "You are registered.\n\nPlease try logging in."
            )

            self.registration_successful.emit(user)


        except Exception as error:


            QMessageBox.critical(

                self,

                "Registration Failed",

                str(error)

            )