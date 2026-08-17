"""
Schedulify Settings Page

Handles:
- Application preferences
- Theme switching
- Notification preferences

Connects:
UI → SettingsController → SettingsService
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QComboBox,
    QMessageBox
)


from controllers.settings_controller import SettingsController


from ui.settings.theme_manager import ThemeManager



class SettingsPage(QWidget):



    def __init__(
        self,
        settings_controller: SettingsController,
        theme_manager: ThemeManager,
        user
    ):

        super().__init__()


        self.settings_controller = settings_controller

        self.theme_manager = theme_manager

        self.user = user


        self.setup_ui()


        self.load_settings()



    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        self.title = QLabel(
            "Settings"
        )



        self.theme_selector = QComboBox()


        self.theme_selector.addItems(

            [

                "dark",

                "light"

            ]

        )



        self.notification_toggle = QCheckBox(

            "Enable Notifications"

        )



        self.save_button = QPushButton(

            "Save Settings"

        )


        self.save_button.clicked.connect(

            self.save_settings

        )



        widgets = [

            self.title,

            QLabel(
                "Theme"
            ),

            self.theme_selector,

            self.notification_toggle,

            self.save_button

        ]



        for widget in widgets:

            layout.addWidget(
                widget
            )



        self.setLayout(
            layout
        )



    # -------------------------------------------------
    # Load Existing Settings
    # -------------------------------------------------

    def load_settings(
        self
    ):


        try:


            settings = (

                self.settings_controller
                .get_settings(
                    self.user
                )

            )



            self.notification_toggle.setChecked(

                settings.get(

                    "notifications",

                    True

                )

            )


            self.theme_selector.setCurrentText(

                settings.get(

                    "theme",

                    "dark"

                )

            )



        except Exception:


            pass



    # -------------------------------------------------
    # Save Settings
    # -------------------------------------------------

    def save_settings(
        self
    ):


        try:


            theme = (

                self.theme_selector
                .currentText()

            )


            notifications = (

                self.notification_toggle
                .isChecked()

            )



            self.settings_controller.save_settings(

                self.user,

                {

                    "theme": theme,

                    "notifications": notifications

                }

            )



            self.theme_manager.load_theme(

                theme

            )



            QMessageBox.information(

                self,

                "Saved",

                "Settings updated successfully."

            )



        except Exception as error:


            QMessageBox.critical(

                self,

                "Settings Error",

                str(error)

            )