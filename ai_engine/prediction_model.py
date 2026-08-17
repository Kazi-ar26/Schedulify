"""
Schedulify Prediction Model

Provides lightweight predictive analytics.

Responsible for:
- Completion probability estimation
- Workload prediction
- Productivity trend analysis

Designed to work offline.
"""


from statistics import mean

from models.task import Task, TaskStatus
from models.productivity import ProductivityRecord



class PredictionModel:



    def __init__(self):

        self.model_version = "1.0"



    # -------------------------------------------------
    # Task Completion Prediction
    # -------------------------------------------------

    def predict_task_completion(
        self,
        task: Task,
        average_completion_rate: float
    ) -> float:


        score = average_completion_rate



        # Priority adjustment

        if task.priority.value == "high":

            score += 10



        elif task.priority.value == "low":

            score -= 5



        # Deadline pressure

        if task.due_date:

            score += 5



        return round(

            max(
                0,
                min(score, 100)
            ),

            2

        )



    # -------------------------------------------------
    # Workload Prediction
    # -------------------------------------------------

    def predict_workload(
        self,
        tasks: list[Task]
    ) -> str:


        total_duration = sum(

            task.estimated_duration

            for task in tasks

            if task.status != TaskStatus.COMPLETED

        )



        if total_duration > 600:

            return "HIGH"



        if total_duration > 300:

            return "MEDIUM"



        return "LOW"



    # -------------------------------------------------
    # Productivity Trend
    # -------------------------------------------------

    def analyze_productivity_trend(
        self,
        records: list[ProductivityRecord]
    ) -> dict:


        if not records:

            return {

                "trend": "NO_DATA",

                "average_focus_time": 0

            }



        focus_values = [

            record.focus_minutes

            for record in records

        ]


        average_focus = mean(
            focus_values
        )


        recent = records[:3]


        recent_average = mean(

            [

                record.focus_minutes

                for record in recent

            ]

        )



        if recent_average > average_focus:

            trend = "IMPROVING"


        elif recent_average < average_focus:

            trend = "DECLINING"


        else:

            trend = "STABLE"



        return {

            "trend": trend,

            "average_focus_time":

                round(
                    average_focus,
                    2
                )

        }



    # -------------------------------------------------
    # Generate Prediction Summary
    # -------------------------------------------------

    def generate_summary(
        self,
        tasks: list[Task],
        records: list[ProductivityRecord]
    ) -> dict:


        return {

            "workload":

                self.predict_workload(
                    tasks
                ),


            "productivity":

                self.analyze_productivity_trend(
                    records
                )

        }