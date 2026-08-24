"""
Schedulify Settings Page

Handles:
- Application preferences
- Theme switching
- Notification preferences
- Working hours
- Account info
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QComboBox,
    QMessageBox,
    QFrame,
    QScrollArea,
    QSpinBox,
)

from PySide6.QtGui import QFont

from controllers.settings_controller import SettingsController
from ui.settings.theme_manager import ThemeManager


class SettingsPage(QWidget):

    def __init__(
        self,
        settings_controller: SettingsController,
        theme_manager: ThemeManager,
        user: dict,
    ):
        super().__init__()
        self.settings_controller = settings_controller
        self.theme_manager = theme_manager
        self.user = user
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(16)

        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        # ---- Profile Section ----
        profile_frame = self._create_section("Profile")
        pl = profile_frame.layout()

        name = self.user.get("first_name", "") + " " + self.user.get("last_name", "")
        email = self.user.get("email", "")
        role = self.user.get("role", "").title()

        pl.addWidget(self._info_row("Name", name))
        pl.addWidget(self._info_row("Email", email))
        pl.addWidget(self._info_row("Role", role))

        layout.addWidget(profile_frame)

        # ---- Appearance Section ----
        appearance_frame = self._create_section("Appearance")
        al = appearance_frame.layout()

        theme_row = QHBoxLayout()
        theme_lbl = QLabel("Theme")
        theme_lbl.setStyleSheet("color: #9AA2B1; font-size: 14px;")
        theme_row.addWidget(theme_lbl)
        theme_row.addStretch()

        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["dark", "light"])
        self.theme_selector.setMinimumWidth(150)
        self.theme_selector.setMinimumHeight(36)
        self.theme_selector.setStyleSheet("""
            QComboBox {
                background: #111318;
                border: 1px solid #303747;
                border-radius: 8px;
                padding: 6px 12px;
                color: white;
            }
        """)
        theme_row.addWidget(self.theme_selector)
        al.addLayout(theme_row)

        layout.addWidget(appearance_frame)

        # ---- Notifications Section ----
        notif_frame = self._create_section("Notifications")
        nl = notif_frame.layout()

        self.notification_toggle = QCheckBox("Enable notifications")
        self.notification_toggle.setStyleSheet("color: #E8EAED; font-size: 14px;")
        nl.addWidget(self.notification_toggle)

        self.email_toggle = QCheckBox("Email notifications")
        self.email_toggle.setStyleSheet("color: #E8EAED; font-size: 14px;")
        nl.addWidget(self.email_toggle)

        layout.addWidget(notif_frame)

        # ---- Scheduler Section ----
        sched_frame = self._create_section("Scheduler")
        sl = sched_frame.layout()

        self.auto_reschedule = QCheckBox("Auto-reschedule missed tasks")
        self.auto_reschedule.setStyleSheet("color: #E8EAED; font-size: 14px;")
        sl.addWidget(self.auto_reschedule)

        dur_row = QHBoxLayout()
        dur_lbl = QLabel("Default study duration (min)")
        dur_lbl.setStyleSheet("color: #9AA2B1; font-size: 14px;")
        dur_row.addWidget(dur_lbl)
        dur_row.addStretch()

        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(15, 180)
        self.duration_spin.setValue(60)
        self.duration_spin.setMinimumWidth(100)
        self.duration_spin.setStyleSheet("""
            QSpinBox {
                background: #111318;
                border: 1px solid #303747;
                border-radius: 8px;
                padding: 6px 12px;
                color: white;
            }
        """)
        dur_row.addWidget(self.duration_spin)
        sl.addLayout(dur_row)

        layout.addWidget(sched_frame)

        # ---- Save Button ----
        self.save_button = QPushButton("Save Settings")
        self.save_button.setMinimumHeight(44)
        self.save_button.setStyleSheet("""
            QPushButton {
                background: #FFC107;
                color: #111111;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton:hover { background: #FFB300; }
        """)
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        layout.addStretch()
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def load_settings(self):
        try:
            settings = self.settings_controller.get_settings()

            if isinstance(settings, dict):
                self.notification_toggle.setChecked(
                    settings.get("notifications_enabled", True)
                )
                self.email_toggle.setChecked(
                    settings.get("email_notifications", False)
                )
                self.auto_reschedule.setChecked(
                    settings.get("auto_reschedule", True)
                )
                self.duration_spin.setValue(
                    settings.get("default_study_duration", 60)
                )

                dark = settings.get("dark_mode", True)
                self.theme_selector.setCurrentText("dark" if dark else "light")
        except Exception:
            pass

    def save_settings(self):
        try:
            theme = self.theme_selector.currentText()
            notifications = self.notification_toggle.isChecked()

            self.settings_controller.save_settings(
                settings_data={
                    "theme": theme,
                    "notifications": notifications,
                }
            )

            self.theme_manager.load_theme(theme)

            QMessageBox.information(
                self,
                "Saved",
                "Settings updated successfully.",
            )

        except Exception as error:
            QMessageBox.critical(self, "Settings Error", str(error))

    @staticmethod
    def _create_section(title: str) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #171B24;
                border: 1px solid #252B38;
                border-radius: 14px;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        lbl = QLabel(title)
        lbl.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        layout.addWidget(lbl)
        return frame

    @staticmethod
    def _info_row(label: str, value: str) -> QWidget:
        row = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #9AA2B1; font-size: 14px;")
        row.addWidget(lbl)
        row.addStretch()
        val = QLabel(value)
        val.setStyleSheet("color: #E8EAED; font-size: 14px; font-weight: 500;")
        row.addWidget(val)

        container = QWidget()
        container.setLayout(row)
        return container
