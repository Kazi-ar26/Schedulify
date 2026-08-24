"""
Schedulify Test Configuration

Provides:
- In-memory SQLite session for tests
- Fresh tables per test for isolation
"""

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Database.database import Base


# -------------------------------------------------
# Test Engine (in-memory SQLite)
# -------------------------------------------------

TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# -------------------------------------------------
# Create tables before any tests run
# -------------------------------------------------

def pytest_configure(config):
    """Create all tables once at session start."""
    import models  # noqa: F401
    Base.metadata.create_all(bind=test_engine)


# -------------------------------------------------
# Fixtures
# -------------------------------------------------

@pytest.fixture(autouse=True)
def session():
    """
    Provides an isolated database session per test.

    Drops and recreates all tables before each test.
    """
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture
def api_client():
    """Mock API client for testing."""
    from unittest.mock import MagicMock
    from api_client.client import APIClient, get_client
    import api_client.client as client_mod

    mock_client = MagicMock(spec=APIClient)
    original = client_mod._client
    client_mod._client = mock_client

    yield mock_client

    client_mod._client = original
