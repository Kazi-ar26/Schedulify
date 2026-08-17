"""
Schedulify Application Entry Point

Starts:
- Database
- Application
- Theme system
- Main Window
"""


import sys



from PySide6.QtWidgets import QApplication

from Database.database import SessionLocal

from Database.database import init_database


from models.user import User, UserRole
from ui.login.login_page import LoginPage
from ui.login.register_page import RegisterPage
from controllers.auth_controller import AuthController
from ui.main_window import MainWindow


from ui.settings.theme_manager import ThemeManager


from utils.logger import Logger

main_window = None


def main():



    # ---------------------------------------------
    # Initialize Logger
    # ---------------------------------------------

    Logger.info(
        "Starting Schedulify..."
    )



    # ---------------------------------------------
    # Initialize Database
    # ---------------------------------------------

    try:


        init_database()


        Logger.info(
            "Database initialized successfully"
        )


    except Exception as error:


        Logger.error(

            f"Database initialization failed: {error}"

        )



    # ---------------------------------------------
    # Start Qt Application
    # ---------------------------------------------

    app = QApplication(
        sys.argv
    )



    # ---------------------------------------------
    # Load Theme
    # ---------------------------------------------

    theme_manager = ThemeManager(
        app
    )


    theme_manager.load_theme(
        "dark"
    )



    # ---------------------------------------------
    # Authentication Flow
    # ---------------------------------------------

    db = SessionLocal()

    auth_controller = AuthController(db)

    login_page = LoginPage(auth_controller)


    def open_main_window(user: User):

        global main_window


        main_window = MainWindow(
            user,
            theme_manager
        )


        main_window.show()

        login_page.close()

    login_page.login_successful.connect(
        open_main_window
    )

    login_page.show()


    Logger.info(
        "Schedulify launched successfully"
    )


    sys.exit(
        app.exec()
    )




if __name__ == "__main__":

    main()