"""
Schedulify Calendar Controller

Handles:

- Calendar event management
- Event retrieval
- AI schedule retrieval
- Calendar synchronization

Connects:
UI → Controller → Calendar/Event Services
"""

from datetime import datetime, date, time, timedelta
import re

from sqlalchemy.orm import Session

from models.student import Student
from models.calendar_event import CalendarEvent
from models.schedule import Schedule


from services.calendar_service import CalendarService
from services.scheduler_service import SchedulerService


class CalendarController:

    def __init__(
        self,
        session: Session
    ):

        self.session = session

        self.calendar_service = CalendarService()

        self.scheduler_service = SchedulerService()


    # -------------------------------------------------
    # Get Student Calendar Events
    # -------------------------------------------------

    def get_events(
        self,
        student: Student
    ) -> list[CalendarEvent]:

        return (

            self.calendar_service
            .get_student_calendar_events(
                self.session,
                student.id
            )

        )


    # -------------------------------------------------
    # Get AI Schedules
    # -------------------------------------------------

    def get_schedules(
        self,
        student: Student
    ):

        return (

            self.scheduler_service
            .get_student_schedules(
                self.session,
                student
            )

        )


    # -------------------------------------------------
    # Create Calendar Event
    # -------------------------------------------------

    def create_event(
        self,
        student: Student,
        title: str,
        description: str,
        start_time: datetime,
        end_time: datetime
    ) -> CalendarEvent:

        event = CalendarEvent(

            student_id=student.id,

            title=title,

            description=description,

            start_time=start_time,

            end_time=end_time

        )

        self.session.add(event)

        self.session.commit()

        self.session.refresh(event)

        return event


    # -------------------------------------------------
    # Delete Calendar Event
    # -------------------------------------------------

    def delete_event(
        self,
        event: CalendarEvent
    ) -> None:

        self.session.delete(event)

        self.session.commit()


    # -------------------------------------------------
    # Upcoming Calendar Events
    # -------------------------------------------------

    def get_upcoming_events(
        self,
        student: Student
    ) -> list[CalendarEvent]:

        now = datetime.now()

        events = self.get_events(
            student
        )

        return [

            event

            for event in events

            if event.start_time > now

        ]
    # -------------------------------------------------
# Get Future Free Slots For Rescheduling
# -------------------------------------------------

    def get_future_free_slots(
        self,
        student,
        schedule
    ):

        slots = []

        now = datetime.now()

        for day in range(1, 8):

            future_date = now + timedelta(days=day)

            # Generate a few reasonable future times
            for hour in range(8, 22):

                slot = future_date.replace(
                    hour=hour,
                    minute=0,
                    second=0,
                    microsecond=0
                )

                slots.append(slot)

        return slots

    # -------------------------------------------------
    # Parse Preferred Study Hours
    # -------------------------------------------------

    def _parse_study_hours(
        self,
        study_hours: str
    ) -> tuple[time, time]:

        value = study_hours.strip()

        # 24-hour format:
        # 16:00-21:00
        match = re.match(
            r"^\s*(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})\s*$",
            value
        )

        if match:

            start_hour = int(match.group(1))
            start_minute = int(match.group(2))

            end_hour = int(match.group(3))
            end_minute = int(match.group(4))

            return (
                time(start_hour, start_minute),
                time(end_hour, end_minute)
            )

        # 12-hour format:
        # 4:00 PM-9:00 PM
        match = re.match(
            r"^\s*(\d{1,2}):(\d{2})\s*(AM|PM)\s*-\s*"
            r"(\d{1,2}):(\d{2})\s*(AM|PM)\s*$",
            value,
            re.IGNORECASE
        )

        if match:

            start_hour = int(match.group(1))
            start_minute = int(match.group(2))
            start_period = match.group(3).upper()

            end_hour = int(match.group(4))
            end_minute = int(match.group(5))
            end_period = match.group(6).upper()

            if start_period == "PM" and start_hour != 12:
                start_hour += 12

            if start_period == "AM" and start_hour == 12:
                start_hour = 0

            if end_period == "PM" and end_hour != 12:
                end_hour += 12

            if end_period == "AM" and end_hour == 12:
                end_hour = 0

            return (
                time(start_hour, start_minute),
                time(end_hour, end_minute)
            )

        raise ValueError(
            "Invalid preferred study hours format. "
            "Use for example '16:00-21:00'."
        )


    # -------------------------------------------------
    # Reschedule Existing Schedule
    # -------------------------------------------------

    def reschedule_schedule(
        self,
        schedule,
        new_start
    ):

        duration = schedule.task.estimated_duration or 60

        new_end = new_start + timedelta(
            minutes=duration
        )

        return self.scheduler_service.reschedule(
            self.session,
            schedule,
            scheduled_date=new_start,
            start_time=new_start.time(),
            end_time=new_end.time()
        )