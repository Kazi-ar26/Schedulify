"""
Schedulify WellBeing Controller

Handles:
- Student wellbeing insights
- Workload analysis
- Recommendations

Connects:
UI → Controller → WellBeing Service
"""


from sqlalchemy.orm import Session

from models.student import Student
from services.wellbeing_service import WellbeingService



class WellBeingController:


    def __init__(
        self,
        session: Session
    ):

        self.session = session

        self.wellbeing_service = WellbeingService()



    # -------------------------------------------------
    # Student Insights
    # -------------------------------------------------

    def get_student_insights(
        self,
        student: Student
    ) -> dict:


        return (

            self.wellbeing_service
            .generate_student_insights(
                self.session,
                student
            )

        )