from concurrent import futures

import grpc
import pytest
from chores.config import Config
from chores.deps import Container, providers
from chores.grpc_generated.chores_pb2_grpc import (
    add_HouseServicer_to_server,
    add_TaskServicer_to_server,
    add_UsersServicer_to_server,
    HouseStub,
    TaskStub,
    UsersStub,
)
from chores.house_server import HouseServer
from chores.interceptors import AuthInterceptor, ExceptionToStatusInterceptor
from chores.models.base import Base
from chores.task_server import TaskServer
from chores.users_server import UsersServer
from cryptography.fernet import Fernet
from grpc_interceptor import ServerInterceptor
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.orm import Session
from sqlalchemy_model_factory import base, Registry
from sqlalchemy_model_factory.pytest import create_registry_fixture

from tests.factories.base import ModelFactory

db = create_postgres_fixture(Base, session=True)
registry = create_registry_fixture(ModelFactory)


@pytest.fixture
def mf_config():
    return {"cleanup": False}


@pytest.fixture
def mf(registry: Registry, db: Session, mf_config: dict):
    with base.ModelFactory(registry, db, options=mf_config) as model_manager:
        yield model_manager


@pytest.fixture
def config(db: Session):
    pmr_credentials = db.pmr_credentials
    return Config(
        **{
            "postgres": {
                "drivername": pmr_credentials.drivername,
                "host": pmr_credentials.host,
                "port": pmr_credentials.port,
                "database": pmr_credentials.database,
                "username": pmr_credentials.username,
                "password": pmr_credentials.password,
            },
            "environment": "test",
            "logging": {"level": "DEBUG"},
            "cryptography": {"secret_key": Fernet.generate_key()},
            "cert": {
                "certs_path": "../../certs/localhost/",
                "hostname": "localhost",
            },
        },
    )


@pytest.fixture
def channel_credentials():
    return grpc.ssl_channel_credentials(
        open("../../certs/localhost/rootCA.crt", "rb").read(),
        open("../../certs/localhost/localhost.key", "rb").read(),
        open("../../certs/localhost/localhost.crt", "rb").read(),
    )


@pytest.fixture
def server_credentials():
    return grpc.ssl_server_credentials(
        [
            (
                open("../../certs/localhost/localhost.key", "rb").read(),
                open("../../certs/localhost/localhost.crt", "rb").read(),
            )
        ],
    )


@pytest.fixture
def container(config: Config, db: Session):
    mock_container = Container()
    mock_container.config.override(providers.Factory(Config, **config.model_dump()))
    mock_container.init_resources()
    mock_container.wire(modules=[".users_server", ".house_server", ".task_server", ".interceptors"])

    yield mock_container


@pytest.fixture
def interceptors():
    return [ExceptionToStatusInterceptor(), AuthInterceptor()]


@pytest.fixture
def user_service(
    container: Container,
    interceptors: list[ServerInterceptor],
    channel_credentials: grpc.ChannelCredentials,
    server_credentials: grpc.ServerCredentials,
):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors)
    add_UsersServicer_to_server(UsersServer(), server)
    port = server.add_secure_port("[::]:50051", server_credentials)
    server.start()

    try:
        with grpc.secure_channel(f"localhost:{port}", channel_credentials) as channel:
            yield UsersStub(channel)
    finally:
        server.stop(None)


@pytest.fixture
def house_service(
    container: Container,
    interceptors: list[ServerInterceptor],
    channel_credentials: grpc.ChannelCredentials,
    server_credentials: grpc.ServerCredentials,
):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors)
    add_HouseServicer_to_server(HouseServer(), server)
    port = server.add_secure_port("[::]:50051", server_credentials)
    server.start()

    try:
        with grpc.secure_channel(f"localhost:{port}", channel_credentials) as channel:
            yield HouseStub(channel)
    finally:
        server.stop(None)


@pytest.fixture
def task_service(
    container: Container,
    interceptors: list[ServerInterceptor],
    channel_credentials: grpc.ChannelCredentials,
    server_credentials: grpc.ServerCredentials,
):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors)
    add_TaskServicer_to_server(TaskServer(), server)
    port = server.add_secure_port("[::]:50051", server_credentials)
    server.start()

    try:
        with grpc.secure_channel(f"localhost:{port}", channel_credentials) as channel:
            yield TaskStub(channel)
    finally:
        server.stop(None)
