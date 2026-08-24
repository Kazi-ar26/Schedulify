"""
Schedulify Smart Scheduler Engine

Responsible for:
- Automatic task scheduling
- Priority-based planning
- Schedule optimization

This module generates recommendations.
Actual database changes are handled by services.
"""


from datetime import datetime, timedelta

from models.task import (
    Task,
    TaskPriority
)


class SmartScheduler:


    def __init__(
        self,
        daily_start_hour: int = 8,
        daily_end_hour: int = 22
    ):

        self.daily_start_hour = daily_start_hour
        self.daily_end_hour = daily_end_hour


    # -------------------------------------------------
    # Task Priority Weight
    # -------------------------------------------------

    @staticmethod
    def get_priority_weight(
        priority: TaskPriority
    ) -> int:


        weights = {

            TaskPriority.HIGH: 3,

            TaskPriority.MEDIUM: 2,

            TaskPriority.LOW: 1

        }


        return weights.get(
            priority,
            1
        )


    # -------------------------------------------------
    # Sort Tasks
    # -------------------------------------------------

    def prioritize_tasks(
        self,
        tasks: list[Task]
    ) -> list[Task]:


        return sorted(

            tasks,

            key=lambda task: (

                -self.get_priority_weight(
                    task.priority
                ),

                task.due_date
                if task.due_date
                else datetime.max

            )

        )


    # -------------------------------------------------
    # Advance to next valid slot
    # -------------------------------------------------

    def _advance_to_next_day(
        self,
        current_time: datetime
    ) -> datetime:
        """Move to the start of the next working day."""

        return (
            current_time
            + timedelta(days=1)
        ).replace(
            hour=self.daily_start_hour,
            minute=0,
            second=0,
            microsecond=0
        )


    # -------------------------------------------------
    # Generate Schedule
    # -------------------------------------------------

    def generate_schedule(
        self,
        tasks: list[Task],
        start_date: datetime
    ) -> list[dict]:


        prioritized_tasks = (
            self.prioritize_tasks(
                tasks
            )
        )


        generated_schedule = []


        current_time = start_date.replace(

            hour=self.daily_start_hour,

            minute=0,

            second=0,

            microsecond=0

        )


        for task in prioritized_tasks:


            duration = timedelta(
                minutes=task.estimated_duration
            )

            end_time = current_time + duration


            # Loop until the task fits within working hours
            while (
                end_time.hour > self.daily_end_hour
                or (
                    end_time.hour == self.daily_end_hour
                    and end_time.minute > 0
                )
            ):

                current_time = (
                    self._advance_to_next_day(
                        current_time
                    )
                )

                end_time = (
                    current_time + duration
                )


            generated_schedule.append({
                "task": task,
                "start_time": current_time,
                "end_time": end_time,
                "generated_by_ai": True
            })

            current_time = end_time + timedelta(
                minutes=15
            )


        return generated_schedule


    # -------------------------------------------------
    # Conflict Detection
    # -------------------------------------------------

    @staticmethod
    def detect_conflicts(
        schedules: list[dict]
    ) -> list[dict]:


        conflicts = []


        for index, current in enumerate(
            schedules
        ):

            for other in schedules[index + 1:]:


                if (

                    current["start_time"]
                    <
                    other["end_time"]

                    and

                    current["end_time"]
                    > other["start_time"]

                ):

                    conflicts.append({

                        "first_task":
                            current["task"],

                        "second_task": other["task"]

                    })


        return conflicts
