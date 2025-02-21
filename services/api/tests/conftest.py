import os

import pytest
from chores_client.config import load_config
from chores_client.main import create_app
from chores_client.routes import all_routes
from fastapi.testclient import TestClient


@pytest.fixture
def test_env():
    os.environ["ENVIRONMENT"] = "test"
    os.environ["LOGGING_LEVEL"] = "INFO"
    os.environ["SERVICE_BASE_URL"] = "localhost"
    os.environ["USER_SERVICE_PORT"] = "50051"
    os.environ["HOUSE_SERVICE_PORT"] = "50052"
    os.environ["TASK_SERVICE_PORT"] = "50053"
    os.environ["CERTS_PATH"] = "../../certs/localhost"


@pytest.fixture
def config(test_env):
    return load_config()


@pytest.fixture
def client():
    app = create_app(all_routes)

    test_client = TestClient(app)
    return test_client
