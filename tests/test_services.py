"""
Service Layer Tests

Tests:
- User service
- Task service
- Notification service
- Analytics service

Ensures business logic works correctly.
"""


import pytest


from Database.session import get_test_session


from services.user_service import UserService

from services.task_service import TaskService

from services.notification_service import NotificationService

from services.analytics_service import AnalyticsService



@pytest.fixture
def session():

    db = get_test_session()

    yield db

    db.rollback()

    db.close()



@pytest.fixture
def user_service(
    session
):

    return UserService(
        session
    )



@pytest.fixture
def task_service(
    session
):

    return TaskService(
        session
    )



@pytest.fixture
def notification_service(
    session
):

    return NotificationService(
        session
    )



@pytest.fixture
def analytics_service(
    session
):

    return AnalyticsService(
        session
    )



# -------------------------------------------------
# User Service Tests
# -------------------------------------------------

def test_get_user(
    user_service
):


    user = user_service.get_user_by_email(

        "test@test.com"

    )


    assert (

        user is None

        or

        user.email == "test@test.com"

    )



# -------------------------------------------------
# Task Service Tests
# -------------------------------------------------

def test_create_task(
    task_service
):


    task = task_service.create_task(

        {

            "title":

                "Complete Physics Revision",


            "description":

                "Chapter revision",


            "priority":

                "High"

        }

    )



    assert task is not None



def test_task_priority(
    task_service
):


    task = task_service.create_task(

        {

            "title":

                "Important Assignment",


            "priority":

                "Urgent"

        }

    )


    assert task.priority == "Urgent"



# -------------------------------------------------
# Notification Service Tests
# -------------------------------------------------

def test_create_notification(
    notification_service
):


    notification = (

        notification_service
        .create_notification(

            {

                "title":

                    "Task Reminder",


                "message":

                    "Complete assignment"

            }

        )

    )


    assert notification is not None



# -------------------------------------------------
# Analytics Service Tests
# -------------------------------------------------

def test_generate_analytics(
    analytics_service
):


    analytics = (

        analytics_service
        .generate_productivity_report()

    )


    assert analytics is not None