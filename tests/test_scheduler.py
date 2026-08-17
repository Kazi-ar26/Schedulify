"""
Scheduler Tests

Tests:
- Schedule generation
- Task prioritization
- Automatic rescheduling
"""


import pytest


from datetime import datetime, timedelta


from services.scheduler_service import SchedulerService

from ai_engine.smart_scheduler import SmartScheduler

from ai_engine.rescheduler import Rescheduler



@pytest.fixture
def scheduler():

    return SmartScheduler()



@pytest.fixture
def scheduler_service():

    return SchedulerService()



def create_mock_task(
    title,
    priority,
    duration
):


    return {

        "title": title,

        "priority": priority,

        "duration": duration

    }



def test_scheduler_generates_plan(
    scheduler
):


    tasks = [

        create_mock_task(

            "Physics Revision",

            "High",

            120

        ),

        create_mock_task(

            "Math Practice",

            "Medium",

            60

        )

    ]



    result = scheduler.generate_schedule(

        tasks,

        datetime.now()

    )



    assert result is not None

    assert len(result) == 2



def test_high_priority_task_first(
    scheduler
):


    tasks = [

        create_mock_task(

            "Easy Task",

            "Low",

            30

        ),

        create_mock_task(

            "Important Task",

            "High",

            90

        )

    ]



    result = scheduler.generate_schedule(

        tasks,

        datetime.now()

    )



    assert (

        result[0]["task"]["title"]

        ==

        "Important Task"

    )



def test_rescheduler_moves_task():



    rescheduler = Rescheduler()



    old_schedule = {


        "task": "Assignment",


        "start":

            datetime.now(),

    }



    updated = rescheduler.reschedule(

        old_schedule,

        datetime.now() + timedelta(hours=2)

    )



    assert updated is not None