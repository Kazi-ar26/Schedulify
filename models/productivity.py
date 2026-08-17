"""
Schedulify Productivity ORM Model

Tracks student productivity patterns.

Used for:
- Productivity dashboard
- Analytics
- AI recommendations
"""


from datetime import datetime, timezone


from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    DateTime,
    ForeignKey
)


from sqlalchemy.orm import relationship


from Database.database import Base



class ProductivityRecord(Base):

    __tablename__ = "productivity_records"



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

        back_populates="productivity_records"

    )



    # -------------------------------------------------
    # Productivity Data
    # -------------------------------------------------

    date = Column(

        Date,

        nullable=False

    )


    focus_minutes = Column(

        Integer,

        default=0

    )


    completed_tasks = Column(

        Integer,

        default=0

    )


    missed_tasks = Column(

        Integer,

        default=0

    )


    productivity_score = Column(

        Float,

        default=0.0

    )



    notes = Column(

        String(500),

        nullable=True

    )



    # -------------------------------------------------
    # Timestamp
    # -------------------------------------------------

    created_at = Column(

        DateTime,

        default=lambda: datetime.now(timezone.utc),

        nullable=False

    )



    # -------------------------------------------------
    # Helper
    # -------------------------------------------------

    def calculate_score(self):

        total_tasks = (
            self.completed_tasks +
            self.missed_tasks
        )


        if total_tasks == 0:

            self.productivity_score = 0

            return


        self.productivity_score = (

            self.completed_tasks /
            total_tasks

        ) * 100



    def __repr__(self):

        return (

            f"<ProductivityRecord("
            f"id={self.id}, "
            f"score={self.productivity_score}"
            f")>"

        )