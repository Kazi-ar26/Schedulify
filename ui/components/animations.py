"""
Schedulify Animation Components

Reusable UI animations.

Handles:
- Fade transitions
- Widget movement effects
- Smooth UI interactions

Uses:
- PySide6 Animation Framework
"""


from PySide6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
    QPoint,
    QParallelAnimationGroup
)


from PySide6.QtWidgets import QWidget



class FadeAnimation:



    def __init__(
        self,
        widget: QWidget,
        duration: int = 300
    ):


        self.widget = widget


        self.animation = QPropertyAnimation(

            widget,

            b"windowOpacity"

        )


        self.animation.setDuration(
            duration
        )


        self.animation.setStartValue(
            0.0
        )


        self.animation.setEndValue(
            1.0
        )


        self.animation.setEasingCurve(

            QEasingCurve.InOutQuad

        )



    def start(
        self
    ):

        self.animation.start()



class SlideAnimation:



    def __init__(
        self,
        widget: QWidget,
        start_position: QPoint,
        end_position: QPoint,
        duration: int = 300
    ):


        self.widget = widget


        self.animation = QPropertyAnimation(

            widget,

            b"pos"

        )


        self.animation.setDuration(
            duration
        )


        self.animation.setStartValue(

            start_position

        )


        self.animation.setEndValue(

            end_position

        )


        self.animation.setEasingCurve(

            QEasingCurve.OutCubic

        )



    def start(
        self
    ):

        self.animation.start()



class PageTransition:



    def __init__(
        self,
        old_widget: QWidget,
        new_widget: QWidget
    ):


        self.group = QParallelAnimationGroup()



        self.fade_out = QPropertyAnimation(

            old_widget,

            b"windowOpacity"

        )


        self.fade_in = QPropertyAnimation(

            new_widget,

            b"windowOpacity"

        )



        for animation in [

            self.fade_out,

            self.fade_in

        ]:

            animation.setDuration(
                250
            )


            animation.setEasingCurve(

                QEasingCurve.InOutQuad

            )



        self.group.addAnimation(

            self.fade_out

        )


        self.group.addAnimation(

            self.fade_in

        )



    def start(
        self
    ):

        self.group.start()