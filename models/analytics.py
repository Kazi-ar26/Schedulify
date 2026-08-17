"""
Schedulify Analytics ORM Model

Stores productivity analytics data.

Used for:
- Student dashboards
- Teacher anonymous reports
- AI recommendations
"""


from datetime import datetime, timezone


from sqlalchemy import (
    Column,
    Integer,
    Float,
    Date,
    DateTime,
    ForeignKey
)


from sqlalchemy.orm import relationship


from Database.database import Base



class AnalyticsRecord(Base):

    __tablename__ = "analytics_records"



    # -------------------------------------------------
    # Primary Key
    # -------------------------------------------------

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )



    # -------------------------------------------------
    # Student Relationship
    # -------------------------------------------------

    student_id = Column(

        Integer,

        ForeignKey(
            "students.id",
            ondelete="CASCADE"
        ),

        nullable=False

    )


    student = relationship(

        "Student",

        back_populates="analytics_records"

    )



    # -------------------------------------------------
    # Analytics Data
    # -------------------------------------------------

    record_date = Column(

        Date,

        nullable=False

    )


    completion_rate = Column(

        Float,

        default=0.0

    )


    average_focus_time = Column(

        Float,

        default=0.0

    )


    productivity_score = Column(

        Float,

        default=0.0

    )


    workload_score = Column(

        Float,

        default=0.0

    )



    # -------------------------------------------------
    # Timestamp
    # -------------------------------------------------

    created_at = Column(

        DateTime,

        default=lambda: datetime.now(timezone.utc),

        nullable=False

    )


    updated_at = Column(

        DateTime,

        default=lambda: datetime.now(timezone.utc),

        onupdate=lambda: datetime.now(timezone.utc),

        nullable=False

    )



    # -------------------------------------------------
    # Helper Methods
    # -------------------------------------------------

    def update_productivity_score(self):

        self.productivity_score = (

            self.completion_rate * 0.6 +

            self.average_focus_time * 0.2 +

            self.workload_score * 0.2

        )



    def __repr__(self):

        return (

            f"<AnalyticsRecord("
            f"id={self.id}, "
            f"score={self.productivity_score}"
            f")>"

        )