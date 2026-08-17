"""
Schedulify ORM Models Package

Central export point for all SQLAlchemy models.

Models are imported safely as they are created.
"""



__all__ = [

    "User",

    "Student",

    "Teacher",

    "Task",

    "Schedule",

    "CalendarEvent",

    "Notification",

    "ProductivityRecord",

    "AnalyticsRecord"

]



# -------------------------------------------------
# Safe Model Imports
# -------------------------------------------------

try:
    from models.user import User

except ImportError:
    User = None



try:
    from models.student import Student

except ImportError:
    Student = None



try:
    from models.teacher import Teacher

except ImportError:
    Teacher = None



try:
    from models.task import Task

except ImportError:
    Task = None



try:
    from models.schedule import Schedule

except ImportError:
    Schedule = None



try:
    from models.calendar_event import CalendarEvent

except ImportError:
    CalendarEvent = None



try:
    from models.notification import Notification

except ImportError:
    Notification = None



try:
    from models.productivity import ProductivityRecord

except ImportError:
    ProductivityRecord = None



try:
    from models.analytics import AnalyticsRecord

except ImportError:
    AnalyticsRecord = None