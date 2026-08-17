"""
Schedulify Recommendation Engine

Responsible for:
- Productivity recommendations
- Study suggestions
- Schedule improvement tips

This provides non-clinical productivity advice only.
"""


from models.task import Task, TaskStatus
from models.productivity import ProductivityRecord



class RecommendationEngine:



    def __init__(self):

        self.version = "1.0"



    # -------------------------------------------------
    # Workload Recommendations
    # -------------------------------------------------

    def workload_recommendations(
        self,
        tasks: list[Task]
    ) -> list[str]:


        recommendations = []


        pending_tasks = [

            task

            for task in tasks

            if task.status != TaskStatus.COMPLETED

        ]



        total_duration = sum(

            task.estimated_duration

            for task in pending_tasks

        )



        if total_duration > 600:


            recommendations.append(

                "Your workload is high. Consider splitting large tasks into smaller sessions."

            )



        elif total_duration > 300:


            recommendations.append(

                "Your workload is moderate. Maintain a consistent study schedule."

            )



        else:


            recommendations.append(

                "Your workload is balanced. Continue following your current plan."

            )



        return recommendations



    # -------------------------------------------------
    # Productivity Recommendations
    # -------------------------------------------------

    def productivity_recommendations(
        self,
        records: list[ProductivityRecord]
    ) -> list[str]:


        recommendations = []



        if not records:

            return [

                "Start tracking your study sessions to receive personalized insights."

            ]



        average_focus = sum(

            record.focus_minutes

            for record in records

        ) / len(records)



        if average_focus < 30:


            recommendations.append(

                "Try increasing focused study sessions gradually."

            )



        elif average_focus < 90:


            recommendations.append(

                "Your focus sessions are improving. Keep building consistency."

            )



        else:


            recommendations.append(

                "Your focus duration is strong. Maintain healthy study breaks."

            )



        return recommendations



    # -------------------------------------------------
    # Generate Full Recommendation Report
    # -------------------------------------------------

    def generate_recommendations(
        self,
        tasks: list[Task],
        productivity_records: list[ProductivityRecord]
    ) -> list[str]:


        recommendations = []



        recommendations.extend(

            self.workload_recommendations(
                tasks
            )

        )



        recommendations.extend(

            self.productivity_recommendations(
                productivity_records
            )

        )



        return recommendations