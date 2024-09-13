import pytest
from chores.grpc.users_pb2_grpc import add_UsersServicer_to_server, UsersServicer, UsersStub


@pytest.fixture(scope="module")
def grpc_add_to_server():
    return add_UsersServicer_to_server


@pytest.fixture(scope="module")
def grpc_servicer():
    return UsersServicer()


@pytest.fixture(scope="module")
def grpc_stub_cls(grpc_channel):
    return UsersStub
