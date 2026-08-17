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
    QStackedWidget
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


from models.user import UserRole


from ui.settings.settings_page import SettingsPage
from ui.teacher.anonymous_reports import AnonymousReports

from controllers.dashboard_controller import DashboardController
from controllers.planner_controller import PlannerController
from controllers.calendar_controller import CalendarController
from controllers.analytics_controller import AnalyticsController
from controllers.wellbeing_controller import WellBeingController
from controllers.settings_controller import SettingsController


from Database.database import SessionLocal



class MainWindow(QMainWindow):


    def __init__(
        self,
        user=None,
        theme_manager=None
    ):

        super().__init__()


        self.user = user

        self.theme_manager = theme_manager


        self.setWindowTitle(
            "Schedulify"
        )


        self.setMinimumSize(
            QSize(
                1200,
                750
            )
        )


        self.setup_ui()



    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):

        container = QWidget()


        self.setCentralWidget(
            container
        )


        main_layout = QHBoxLayout(
            container
        )


        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )


        main_layout.setSpacing(
            0
        )


        self.sidebar = Sidebar(
            self.user.role
        )


        self.navbar = Navbar(
            self.user
        )


        self.pages = QStackedWidget()


        self.load_pages()


        main_layout.addWidget(
            self.sidebar
        )


        content_layout = QVBoxLayout()

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        content_layout.setSpacing(
            0
        )

        content_layout.addWidget(
            self.navbar
        )

        content_layout.addWidget(
            self.pages
        )

        main_layout.addLayout(
            content_layout
        )

        self.connect_navigation()

        self.change_page(0)



    # -------------------------------------------------
    # Load Application Pages
    # -------------------------------------------------

    def load_pages(
        self
    ):

        db = SessionLocal()


        dashboard_controller = DashboardController(
            db
        )


        settings_controller = SettingsController(
            db
        )


        # -------------------------------------------------
        # STUDENT
        # -------------------------------------------------

        if self.user.role == UserRole.STUDENT:

            planner_controller = PlannerController(
                db
            )

            calendar_controller = CalendarController(
                db
            )

            analytics_controller = AnalyticsController(
                db
            )

            wellbeing_controller = WellBeingController(
                db
            )


            settings = SettingsPage(
                settings_controller,
                self.theme_manager,
                self.user
            )

            self.student_dashboard = StudentDashboard(
                dashboard_controller,
                self.user.student_profile
            )


            pages = [

                self.student_dashboard,

                PlannerView(
                    planner_controller,
                    self.user.student_profile
                ),

                CalendarView(
                    calendar_controller,
                    self.user.student_profile
                ),

                ProductivityView(
                    analytics_controller,
                    self.user.student_profile
                ),

                WellbeingView(
                    wellbeing_controller,
                    self.user.student_profile
                ),

                settings

            ]


        # -------------------------------------------------
        # TEACHER
        # -------------------------------------------------

        elif self.user.role == UserRole.TEACHER:

            analytics_controller = AnalyticsController(db)

            pages = [

                TeacherDashboard(
                    dashboard_controller,
                    self.user
                ),
                ClassAnalytics(
                    analytics_controller,
                    self.user
                ),

                AnonymousReports(
                    analytics_controller,
                    self.user
                ),

                SettingsPage(
                    settings_controller,
                    self.theme_manager,
                    self.user
                )
            ]


        # -------------------------------------------------
        # UNKNOWN ROLE
        # -------------------------------------------------

        else:

            pages = []


        for page in pages:

            self.add_page(
                page
            )



    # -------------------------------------------------
    # Navigation Handling
    # -------------------------------------------------

    def connect_navigation(
        self
    ):

        self.sidebar.page_changed.connect(
            self.change_page
        )



    def change_page(
        self,
        index: int
    ):

        if 0 <= index < self.pages.count():

            self.pages.setCurrentIndex(index)

            # -----------------------------------------
            # Navbar Title
            # -----------------------------------------

            if self.user.role == UserRole.STUDENT:

                titles = [
                    "Dashboard",
                    "Planner",
                    "Calendar",
                    "Productivity",
                    "Wellbeing",
                    "Settings"
                ]

            else:

                titles = [
                    "Dashboard",
                    "Class Analytics",
                    "Anonymous Reports",
                    "Settings"
                ]

            self.navbar.set_page_title(
                titles[index]
            )

            current_page = self.pages.currentWidget()

            if hasattr(
                current_page,
                "load_dashboard"
            ):

                current_page.load_dashboard()



    # -------------------------------------------------
    # Add Pages
    # -------------------------------------------------

    def add_page(
        self,
        widget: QWidget
    ):

        self.pages.addWidget(
            widget
        )



    # -------------------------------------------------
    # Theme Support
    # -------------------------------------------------

    def apply_theme(
        self,
        stylesheet: str
    ):

        self.setStyleSheet(
            stylesheet
        )