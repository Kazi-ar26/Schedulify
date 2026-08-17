"""
Schedulify Theme Manager

Handles:
- Application themes
- QSS stylesheet loading
- Dark/light mode switching

Connects:
Settings UI → ThemeManager → QApplication
"""


import os


from PySide6.QtWidgets import QApplication



class ThemeManager:



    def __init__(
        self,
        app: QApplication
    ):


        self.app = app


        self.current_theme = "dark"



    # -------------------------------------------------
    # Load Theme
    # -------------------------------------------------

    def load_theme(
        self,
        theme: str
    ):


        stylesheet = self.get_stylesheet(
            theme
        )


        self.app.setStyleSheet(
            stylesheet
        )


        self.current_theme = theme



    # -------------------------------------------------
    # Read QSS File
    # -------------------------------------------------

    def get_stylesheet(
        self,
        theme: str
    ):


        base_path = os.path.dirname(

            os.path.dirname(

                os.path.dirname(

                    os.path.abspath(__file__)

                )

            )

        )



        style_path = os.path.join(

            base_path,

            "styles",

            f"{theme}.qss"

        )



        if not os.path.exists(
            style_path
        ):


            return ""



        with open(

            style_path,

            "r",

            encoding="utf-8"

        ) as file:


            return file.read()



    # -------------------------------------------------
    # Toggle Theme
    # -------------------------------------------------

    def toggle_theme(
        self
    ):


        if self.current_theme == "dark":


            self.load_theme(
                "light"
            )


        else:


            self.load_theme(
                "dark"
            )