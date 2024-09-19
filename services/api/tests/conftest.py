from concurrent import futures

import grpc
import pytest
from chores.config import Config
from chores.deps import Container, providers
from chores.grpc_generated.users_pb2_grpc import add_UsersServicer_to_server, UsersStub
from chores.models.base import Base
from chores.users_server import UsersServer
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy.orm import Session

db = create_postgres_fixture(Base, session=True)


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
        },
    )


@pytest.fixture
def container(config: Config, db: Session):
    mock_container = Container()
    mock_container.config.override(providers.Factory(Config, **config.model_dump()))
    mock_container.init_resources()

    yield mock_container


@pytest.fixture
def user_service(container: Container):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UsersServicer_to_server(UsersServer(), server)
    port = server.add_insecure_port("[::]:0")
    server.start()

    try:
        with grpc.insecure_channel("localhost:%d" % port) as channel:
            yield UsersStub(channel)
    finally:
        server.stop(None)