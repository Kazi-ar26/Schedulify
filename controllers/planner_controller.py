"""
Schedulify Planner Controller

Handles:
- Task planning
- Schedule generation
- Automatic scheduling
- Rescheduling workflows

Connects:
UI → Controller → Services → AI Engine
"""


from datetime import datetime


from sqlalchemy.orm import Session


from models.student import Student
from models.task import Task


from services.task_service import TaskService
from services.scheduler_service import SchedulerService


from ai_engine.smart_scheduler import SmartScheduler
from ai_engine.rescheduler import Rescheduler



class PlannerController:



    def __init__(
        self,
        session: Session
    ):

        self.session = session

        self.task_service = TaskService()

        self.scheduler_service = SchedulerService()

        self.smart_scheduler = SmartScheduler()

        self.rescheduler = Rescheduler()



    # -------------------------------------------------
    # Task Retrieval
    # -------------------------------------------------

    def get_student_tasks(
        self,
        student: Student
    ) -> list[Task]:


        return (

            self.task_service
            .get_student_tasks(
                self.session,
                student
            )

        )

    # -------------------------------------------------
    # Create Task
    # -------------------------------------------------

    def create_task(
        self,
        student: Student,
        *,
        title: str,
        description: str | None = None,
        category: str | None = None,
        priority=None,
        estimated_duration: int = 60,
        due_date: datetime | None = None
    ) -> Task:


        return (

            self.task_service
            .create_task(
                self.session,

                student=student,

                title=title,

                description=description,

                category=category,

                priority=priority,

                estimated_duration=estimated_duration,

                due_date=due_date

            )

        )


    # -------------------------------------------------
    # Generate AI Schedule
    # -------------------------------------------------

    def generate_schedule(
        self,
        student: Student,
        start_date: datetime
    ) -> list[dict]:


        tasks = (

            self.task_service
            .get_unscheduled_tasks(
                self.session,
                student
            )

        )


        schedule_plan = (

            self.smart_scheduler
            .generate_schedule(
                tasks,
                start_date
            )

        )


        return schedule_plan



    # -------------------------------------------------
    # Save Generated Schedule
    # -------------------------------------------------

    def save_schedule(
        self,
        student: Student,
        schedule_plan: list[dict]
    ):


        created = []


        for item in schedule_plan:


            schedule = (

                self.scheduler_service
                .create_schedule(
                    self.session,

                    student=student,

                    task=item["task"],

                    scheduled_date=item["start_time"].date(),

                    start_time=item["start_time"],

                    end_time=item["end_time"],

                    generated_by_ai=True

                )

            )


            created.append(schedule)



        return created



    # -------------------------------------------------
    # Reschedule Missed Tasks
    # -------------------------------------------------

    def reschedule_tasks(
        self,
        student: Student,
        current_time: datetime
    ) -> list[dict]:


        missed_tasks = (

            self.task_service
            .get_missed_tasks(
                self.session,
                student
            )

        )


        existing_schedule = (

            self.scheduler_service
            .get_student_schedule(
                self.session,
                student
            )

        )


        return (

            self.rescheduler
            .reschedule_multiple_tasks(
                missed_tasks,

                existing_schedule,

                current_time

            )

        )



    # -------------------------------------------------
    # Daily Planner Data
    # -------------------------------------------------

    def get_daily_plan(
        self,
        student: Student,
        date
    ):


        return (

            self.scheduler_service
            .get_daily_schedule(
                self.session,
                student,
                date
            )

        )