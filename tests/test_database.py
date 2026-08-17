"""
Database Tests

Tests:
- Database connection
- Session creation
- Model persistence
- Basic CRUD operations
"""


import pytest


from Database.session import get_test_session


from models.user import User



@pytest.fixture
def session():

    db = get_test_session()

    yield db

    db.rollback()

    db.close()



def test_database_connection(
    session
):


    assert session is not None



def test_create_user(
    session
):


    user = User(

        first_name="Database",

        last_name="Test",

        email="database@test.com",

        password_hash="hashed_password",

        role="Student"

    )


    session.add(
        user
    )


    session.commit()



    result = session.query(

        User

    ).filter_by(

        email="database@test.com"

    ).first()



    assert result is not None

    assert result.email == "database@test.com"



def test_user_persistence(
    session
):


    users_before = session.query(

        User

    ).count()



    user = User(

        first_name="Persistence",

        last_name="Check",

        email="persist@test.com",

        password_hash="hash",

        role="Teacher"

    )


    session.add(
        user
    )


    session.commit()



    users_after = session.query(

        User

    ).count()



    assert users_after == users_before + 1