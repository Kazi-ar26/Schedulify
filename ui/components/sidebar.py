from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel
)

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap

import qtawesome as qta

from models.user import UserRole


class Sidebar(QWidget):

    page_changed = Signal(int)
    switch_user_requested = Signal()

    def __init__(
        self,
        role: UserRole
    ):

        super().__init__()

        self.role = role
        self.buttons = []

        self.setup_ui()


    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            12,
            18,
            12,
            14
        )

        layout.setSpacing(5)

        self.setObjectName(
            "sidebar"
        )

        self.setFixedWidth(
            250
        )


        # -------------------------------------------------
        # Logo
        # -------------------------------------------------

        self.logo = QLabel()

        self.logo.setObjectName(
            "sidebarLogo"
        )

        self.logo.setAlignment(
            Qt.AlignmentFlag.AlignLeft |
            Qt.AlignmentFlag.AlignVCenter
        )

        logo_path = (
            Path(__file__).resolve().parents[2]
            / "Assets"
            / "icons"
            / "schedulify_logo.png"
        )

        logo_pixmap = QPixmap(
            str(logo_path)
        )

        if not logo_pixmap.isNull():

            self.logo.setPixmap(
                logo_pixmap.scaled(
                    175,
                    70,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

        else:

            # Fallback if the image cannot be found
            self.logo.setText(
                "Schedulify"
            )

        layout.addWidget(
            self.logo
        )


        # -------------------------------------------------
        # Navigation
        # -------------------------------------------------

        if self.role == UserRole.STUDENT:

            self.add_navigation_button(
                layout,
                "Dashboard",
                "mdi.view-dashboard-outline",
                0
            )

            self.add_navigation_button(
                layout,
                "Planner",
                "mdi.notebook-outline",
                1
            )

            self.add_navigation_button(
                layout,
                "Calendar",
                "mdi.calendar-month-outline",
                2
            )

            self.add_navigation_button(
                layout,
                "Productivity",
                "mdi.chart-line",
                3
            )

            self.add_navigation_button(
                layout,
                "Wellbeing",
                "mdi.heart-pulse",
                4
            )


        elif self.role == UserRole.TEACHER:

            self.add_navigation_button(
                layout,
                "Dashboard",
                "mdi.view-dashboard-outline",
                0
            )

            self.add_navigation_button(
                layout,
                "Class Analytics",
                "mdi.chart-box-outline",
                1
            )

            self.add_navigation_button(
                layout,
                "Anonymous Reports",
                "mdi.file-chart-outline",
                2
            )


        # -------------------------------------------------
        # Push utility buttons to bottom
        # -------------------------------------------------

        layout.addStretch()


        # -------------------------------------------------
        # Switch User
        # -------------------------------------------------

        self.switch_user_button = QPushButton(
            "Switch User"
        )

        self.switch_user_button.setObjectName(
            "sidebarUtilityButton"
        )

        self.switch_user_button.setIcon(
            qta.icon(
                "mdi.account-switch-outline",
                color="#9AA2B1",
                color_active="#FFC107"
            )
        )

        self.switch_user_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.switch_user_button.clicked.connect(
            self.switch_user_requested.emit
        )

        layout.addWidget(
            self.switch_user_button
        )


        # -------------------------------------------------
        # Settings
        # -------------------------------------------------

        settings_index = (
            5
            if self.role == UserRole.STUDENT
            else 3
        )

        self.settings_button = QPushButton(
            "Settings"
        )

        self.settings_button.setObjectName(
            "sidebarUtilityButton"
        )

        self.settings_button.setIcon(
            qta.icon(
                "mdi.cog-outline",
                color="#9AA2B1",
                color_active="#FFC107"
            )
        )

        self.settings_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.settings_button.clicked.connect(
            lambda:
            self.handle_navigation(
                settings_index
            )
        )

        layout.addWidget(
            self.settings_button
        )


        # -------------------------------------------------
        # Default Active Page
        # -------------------------------------------------

        self.set_active_page(
            0
        )


    # -------------------------------------------------
    # Create Navigation Button
    # -------------------------------------------------

    def add_navigation_button(
        self,
        layout,
        text,
        icon_name,
        page_index
    ):

        button = QPushButton(
            text
        )

        button.setObjectName(
            "sidebarButton"
        )

        button.setIcon(
            qta.icon(
                icon_name,
                color="#9AA2B1",
                color_active="#FFC107"
            )
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setProperty(
            "active",
            False
        )

        button.clicked.connect(
            lambda checked=False,
                   index=page_index:
            self.handle_navigation(
                index
            )
        )

        self.buttons.append(
            button
        )

        layout.addWidget(
            button
        )


    # -------------------------------------------------
    # Navigation
    # -------------------------------------------------

    def handle_navigation(
        self,
        index
    ):

        self.set_active_page(
            index
        )

        self.page_changed.emit(
            index
        )


    # -------------------------------------------------
    # Active Page
    # -------------------------------------------------

    def set_active_page(
        self,
        index
    ):

        for button_index, button in enumerate(
            self.buttons
        ):

            is_active = (
                button_index == index
            )

            button.setProperty(
                "active",
                is_active
            )

            button.style().unpolish(
                button
            )

            button.style().polish(
                button
            )

            button.update()