import os
from concurrent import futures

import grpc
import pytest
from chores.grpc_generated.chores_pb2_grpc import (
    add_HouseServicer_to_server,
    add_TaskServicer_to_server,
    add_UsersServicer_to_server,
    HouseStub,
    TaskStub,
    UsersStub,
)
from chores.house_server import HouseServer
from chores.task_server import TaskServer
from chores.users_server import UsersServer
from chores_client.config import Config, load_config
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


@pytest.fixture
def config(test_env):
    return load_config()


@pytest.fixture
def client():
    app = create_app(all_routes)

    test_client = TestClient(app)
    return test_client


@pytest.fixture
def user_service(config: Config):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UsersServicer_to_server(UsersServer(), server)
    port = server.add_insecure_port(config.chores_service.user_service_url)
    server.start()

    try:
        with grpc.insecure_channel(f"localhost:{port}") as channel:
            yield UsersStub(channel)
    finally:
        server.stop(None)


@pytest.fixture
def house_service(config: Config):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_HouseServicer_to_server(HouseServer(), server)
    port = server.add_insecure_port(config.chores_service.house_service_url)
    server.start()

    try:
        with grpc.insecure_channel(f"localhost:{port}") as channel:
            yield HouseStub(channel)
    finally:
        server.stop(None)


@pytest.fixture
def task_service(config: Config):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TaskServicer_to_server(TaskServer(), server)
    port = server.add_insecure_port(f"[::]:{config.chores_service.task_service_port}")
    server.start()

    try:
        with grpc.insecure_channel(f"localhost:{port}") as channel:
            yield TaskStub(channel)
    finally:
        server.stop(None)
