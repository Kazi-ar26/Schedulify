"""
Schedulify Application Constants

Central storage for:
- Application metadata
- User roles
- Task states
- Priorities
- Theme values
- Shared configuration
"""


# -------------------------------------------------
# Application Information
# -------------------------------------------------

APP_NAME = "Schedulify"

APP_VERSION = "1.0.0"



# -------------------------------------------------
# User Roles
# -------------------------------------------------

ROLE_STUDENT = "Student"

ROLE_TEACHER = "Teacher"



USER_ROLES = [

    ROLE_STUDENT,

    ROLE_TEACHER

]



# -------------------------------------------------
# Task Priorities
# -------------------------------------------------

PRIORITY_LOW = "Low"

PRIORITY_MEDIUM = "Medium"

PRIORITY_HIGH = "High"

PRIORITY_URGENT = "Urgent"



TASK_PRIORITIES = [

    PRIORITY_LOW,

    PRIORITY_MEDIUM,

    PRIORITY_HIGH,

    PRIORITY_URGENT

]



# -------------------------------------------------
# Task Status
# -------------------------------------------------

STATUS_PENDING = "Pending"

STATUS_IN_PROGRESS = "In Progress"

STATUS_COMPLETED = "Completed"

STATUS_CANCELLED = "Cancelled"



TASK_STATUSES = [

    STATUS_PENDING,

    STATUS_IN_PROGRESS,

    STATUS_COMPLETED,

    STATUS_CANCELLED

]



# -------------------------------------------------
# Theme Constants
# -------------------------------------------------

THEME_DARK = "dark"

THEME_LIGHT = "light"



AVAILABLE_THEMES = [

    THEME_DARK,

    THEME_LIGHT

]



# -------------------------------------------------
# AI Scheduler Settings
# -------------------------------------------------

DEFAULT_WORKING_HOURS = 8

DEFAULT_FOCUS_DURATION = 50

DEFAULT_BREAK_DURATION = 10



# -------------------------------------------------
# Notification Types
# -------------------------------------------------

NOTIFICATION_TASK = "Task"

NOTIFICATION_SCHEDULE = "Schedule"

NOTIFICATION_SYSTEM = "System"



NOTIFICATION_TYPES = [

    NOTIFICATION_TASK,

    NOTIFICATION_SCHEDULE,

    NOTIFICATION_SYSTEM

]