"""
Schedulify Navbar Component
"""

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton
)

from PySide6.QtCore import (
    Signal,
    Qt,
    QSize
)

import qtawesome as qta


class Navbar(QWidget):

    notification_clicked = Signal()
    theme_toggle_requested = Signal()

    def __init__(
        self,
        user=None,
        page_title="Dashboard"
    ):

        super().__init__()

        self.user = user
        self.page_title = page_title

        self.setup_ui()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def setup_ui(self):

        self.setObjectName("navbar")
        self.setFixedHeight(72)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            24,
            14,
            24,
            14
        )

        layout.setSpacing(14)

        # -------------------------------------------------
        # Page Title
        # -------------------------------------------------

        self.title = QLabel(
            self.page_title
        )

        self.title.setObjectName(
            "navbarTitle"
        )

        layout.addWidget(
            self.title
        )

        layout.addStretch()

        # -------------------------------------------------
        # Notification Button
        # -------------------------------------------------

        self.notification_button = QPushButton()

        self.notification_button.setObjectName(
            "navbarIconButton"
        )

        self.notification_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.notification_button.setIcon(
            qta.icon(
                "mdi.bell-outline",
                color="#AEB7C8"
            )
        )

        self.notification_button.setIconSize(
            QSize(20, 20)
        )

        self.notification_button.clicked.connect(
            self.notification_clicked.emit
        )

        layout.addWidget(
            self.notification_button
        )

        # -------------------------------------------------
        # Theme Button
        # -------------------------------------------------

        self.theme_button = QPushButton()

        self.theme_button.setObjectName(
            "navbarIconButton"
        )

        self.theme_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.theme_button.setIcon(
            qta.icon(
                "mdi.weather-night",
                color="#AEB7C8"
            )
        )

        self.theme_button.setIconSize(
            QSize(20, 20)
        )

        self.theme_button.clicked.connect(
            self.theme_toggle_requested.emit
        )

        layout.addWidget(
            self.theme_button
        )

        # -------------------------------------------------
        # User Badge
        # -------------------------------------------------

        self.user_label = QLabel(
            self.get_user_display()
        )

        self.user_label.setObjectName(
            "navbarUser"
        )

        self.user_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.user_label
        )

    # -------------------------------------------------
    # User Display
    # -------------------------------------------------

    def get_user_display(self):

        if self.user:

            first = getattr(
                self.user,
                "first_name",
                ""
            )

            last = getattr(
                self.user,
                "last_name",
                ""
            )

            return f"{first} {last}".strip()

        return "Guest"

    # -------------------------------------------------
    # Update User
    # -------------------------------------------------

    def set_user(
        self,
        user
    ):

        self.user = user

        self.user_label.setText(
            self.get_user_display()
        )

    # -------------------------------------------------
    # Update Title
    # -------------------------------------------------

    def set_page_title(
        self,
        title
    ):

        self.page_title = title

        self.title.setText(
            title
        )