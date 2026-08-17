"""
Schedulify Automatic Rescheduler

Responsible for:
- Detecting scheduling conflicts
- Finding alternative slots
- Generating rescheduling suggestions

Database updates are handled by services.
"""


from datetime import datetime, timedelta

from models.task import Task



class Rescheduler:



    def __init__(
        self,
        working_start_hour: int = 8,
        working_end_hour: int = 22
    ):

        self.working_start_hour = working_start_hour

        self.working_end_hour = working_end_hour



    # -------------------------------------------------
    # Calculate Task Duration
    # -------------------------------------------------

    @staticmethod
    def get_duration(
        task: Task
    ) -> timedelta:


        return timedelta(

            minutes=task.estimated_duration

        )



    # -------------------------------------------------
    # Find Next Available Slot
    # -------------------------------------------------

    def find_available_slot(
        self,
        existing_schedules: list[dict],
        task: Task,
        start_from: datetime
    ) -> dict | None:


        current_time = start_from.replace(

            hour=self.working_start_hour,

            minute=0,

            second=0,

            microsecond=0

        )


        duration = self.get_duration(
            task
        )


        search_until = start_from + timedelta(days=7)

        while current_time <= search_until:


            end_time = current_time + duration



            if end_time.hour <= self.working_end_hour:


                conflict = False



                for schedule in existing_schedules:

                    if isinstance(schedule, dict):

                        schedule_start = schedule["start_time"]
                        schedule_end = schedule["end_time"]

                    else:

                        schedule_start = schedule.start_time
                        schedule_end = schedule.end_time

                    if (
                        current_time < schedule_end
                        and end_time > schedule_start
                    ):

                        conflict = True

                        break



                if not conflict:

                    return {

                        "task": task,

                        "start_time": current_time,

                        "end_time": end_time,

                        "reason":

                            "Automatically rescheduled"

                    }



            current_time += timedelta(

                minutes=30

            )



        return None



    # -------------------------------------------------
    # Reschedule Missed Task
    # -------------------------------------------------

    def reschedule_task(
        self,
        task: Task,
        existing_schedules: list[dict],
        current_time: datetime
    ) -> dict | None:


        return self.find_available_slot(

            existing_schedules,

            task,

            current_time

        )



    # -------------------------------------------------
    # Handle Multiple Missed Tasks
    # -------------------------------------------------

    def reschedule_multiple_tasks(
        self,
        tasks: list[Task],
        existing_schedules: list[dict],
        current_time: datetime
    ) -> list[dict]:


        suggestions = []



        for task in tasks:


            suggestion = (

                self.reschedule_task(

                    task,

                    existing_schedules,

                    current_time

                )

            )



            if suggestion:


                suggestions.append(
                    suggestion
                )


        return suggestions