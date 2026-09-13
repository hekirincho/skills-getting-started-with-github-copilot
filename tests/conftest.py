import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Store initial state of activities for resetting before each test
INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dict before every test to maintain test isolation."""
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


@pytest.fixture
def client():
    """Fixture providing a FastAPI TestClient instance."""
    return TestClient(app)
