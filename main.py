"""
Schedulify Application Entry Point

Starts:
- API Client connection
- Application
- Theme system
- Main Window
"""

import sys

from PySide6.QtWidgets import QApplication

from ui.login.login_page import LoginPage
from controllers.auth_controller import AuthController
from ui.main_window import MainWindow

from ui.settings.theme_manager import ThemeManager

from utils.logger import Logger

from api_client.client import load_token, load_user_data, clear_token


main_window = None


def main():

    global main_window

    # ---------------------------------------------
    # Initialize Logger
    # ---------------------------------------------

    Logger.info("Starting Schedulify v2.0...")

    # ---------------------------------------------
    # Start Qt Application
    # ---------------------------------------------

    app = QApplication(sys.argv)

    # ---------------------------------------------
    # Load Theme
    # ---------------------------------------------

    theme_manager = ThemeManager(app)
    theme_manager.load_theme("dark")

    # ---------------------------------------------
    # Check for existing session
    # ---------------------------------------------

    existing_token = load_token()
    existing_user = load_user_data()

    if existing_token and existing_user:
        Logger.info("Found existing session, verifying...")

        from api_client.client import get_client
        client = get_client()
        client.set_token(existing_token)

        try:
            from api_client.auth_api import get_me
            me_result = get_me()

            if me_result and "user" in me_result:
                user_data = me_result["user"]
                profile = me_result.get("profile")
                user_data["profile"] = profile

                main_window = MainWindow(user_data, theme_manager)
                main_window.show()
                Logger.info("Resumed session successfully.")
                sys.exit(app.exec())
                return
        except Exception as e:
            Logger.info(f"Session expired: {e}")
            clear_token()

    # ---------------------------------------------
    # Authentication Flow
    # ---------------------------------------------

    auth_controller = AuthController()
    login_page = LoginPage(auth_controller)

    def open_main_window(user: dict):

        global main_window

        main_window = MainWindow(user, theme_manager)
        main_window.show()
        login_page.close()

    login_page.login_successful.connect(open_main_window)
    login_page.show()

    Logger.info("Schedulify launched successfully")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
