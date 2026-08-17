"""
Schedulify Calendar Service

Handles student calendar event operations.
"""


from sqlalchemy.orm import Session

from models.calendar_event import CalendarEvent



class CalendarService:


    @staticmethod
    def get_student_calendar_events(
        session: Session,
        student_id: int
    ):

        return (
            session.query(CalendarEvent)
            .filter(
                CalendarEvent.student_id == student_id
            )
            .order_by(
                CalendarEvent.start_time
            )
            .all()
        )
    