"""
Schedulify Main Window

Application shell responsible for:
- Window initialization
- Navigation container
- Page switching
- Global UI layout

Built using PySide6.
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
)

from PySide6.QtCore import QSize

from ui.components.sidebar import Sidebar
from ui.components.navbar import Navbar

from ui.student.student_dashboard import StudentDashboard
from ui.student.planner_view import PlannerView
from ui.student.calendar_view import CalendarView
from ui.student.productivity_view import ProductivityView
from ui.student.wellbeing_view import WellbeingView

from ui.teacher.class_analytics import ClassAnalytics
from ui.teacher.teacher_dashboard import TeacherDashboard

from ui.settings.settings_page import SettingsPage
from ui.teacher.anonymous_reports import AnonymousReports

from controllers.dashboard_controller import DashboardController
from controllers.planner_controller import PlannerController
from controllers.calendar_controller import CalendarController
from controllers.analytics_controller import AnalyticsController
from controllers.wellbeing_controller import WellBeingController
from controllers.settings_controller import SettingsController

from models.user import UserRole

from api_client.auth_api import logout


class MainWindow(QMainWindow):

    def __init__(self, user: dict = None, theme_manager=None):
        super().__init__()

        self.user = user or {}
        self.theme_manager = theme_manager

        self.setWindowTitle("Schedulify")
        self.setMinimumSize(QSize(1200, 750))

        self.setup_ui()

    def setup_ui(self):
        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Determine role
        role_str = self.user.get("role", "student")
        role = (
            UserRole.STUDENT
            if role_str == "student"
            else UserRole.TEACHER
        )

        self.sidebar = Sidebar(role)
        self.navbar = Navbar(
            self._make_user_for_navbar(),
        )

        self.pages = QStackedWidget()
        self.load_pages(role)

        main_layout.addWidget(self.sidebar)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(self.navbar)
        content_layout.addWidget(self.pages)

        main_layout.addLayout(content_layout)

        self.sidebar.page_changed.connect(self.change_page)
        self.sidebar.switch_user_requested.connect(self._handle_logout)
        self.change_page(0)

    def _make_user_for_navbar(self):
        """Create a simple object for the navbar to read name from."""

        class _User:
            pass

        u = _User()
        u.first_name = self.user.get("first_name", "")
        u.last_name = self.user.get("last_name", "")
        return u

    def load_pages(self, role: UserRole):
        dashboard_controller = DashboardController()
        settings_controller = SettingsController()

        if role == UserRole.STUDENT:
            planner_controller = PlannerController()
            calendar_controller = CalendarController()
            analytics_controller = AnalyticsController()
            wellbeing_controller = WellBeingController()

            settings = SettingsPage(
                settings_controller,
                self.theme_manager,
                self.user,
            )

            student_id = self.user.get("profile", {})
            if student_id and isinstance(student_id, dict):
                student_id = student_id.get("id")
            else:
                student_id = self.user.get("id", 0)

            self.student_dashboard = StudentDashboard(
                dashboard_controller,
                self.user,
            )

            pages = [
                self.student_dashboard,
                PlannerView(planner_controller, self.user),
                CalendarView(calendar_controller, self.user),
                ProductivityView(analytics_controller, self.user),
                WellbeingView(wellbeing_controller, self.user),
                settings,
            ]

        elif role == UserRole.TEACHER:
            analytics_controller = AnalyticsController()
            pages = [
                TeacherDashboard(dashboard_controller, self.user),
                ClassAnalytics(analytics_controller, self.user),
                AnonymousReports(analytics_controller, self.user),
                SettingsPage(settings_controller, self.theme_manager, self.user),
            ]
        else:
            pages = []

        for page in pages:
            self.add_page(page)

    def change_page(self, index: int):
        if 0 <= index < self.pages.count():
            self.pages.setCurrentIndex(index)

            role_str = self.user.get("role", "student")

            if role_str == "student":
                titles = [
                    "Dashboard", "Planner", "Calendar",
                    "Productivity", "Wellbeing", "Settings",
                ]
            else:
                titles = [
                    "Dashboard", "Class Analytics",
                    "Anonymous Reports", "Settings",
                ]

            if index < len(titles):
                self.navbar.set_page_title(titles[index])

            current_page = self.pages.currentWidget()
            if hasattr(current_page, "load_dashboard"):
                current_page.load_dashboard()

    def add_page(self, widget: QWidget):
        self.pages.addWidget(widget)

    def _handle_logout(self):
        logout()
        from api_client.client import clear_token
        clear_token()
        self.close()

        # Relaunch login
        from ui.login.login_page import LoginPage
        from controllers.auth_controller import AuthController

        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()

        auth_controller = AuthController()
        login_page = LoginPage(auth_controller)

        def open_main(user: dict):
            global main_window
            from ui.main_window import MainWindow as MW
            main_window = MW(user, self.theme_manager)
            main_window.show()
            login_page.close()

        login_page.login_successful.connect(open_main)
        login_page.show()

    def apply_theme(self, stylesheet: str):
        self.setStyleSheet(stylesheet)
