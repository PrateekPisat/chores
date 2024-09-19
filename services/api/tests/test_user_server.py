from chores.grpc_generated.users_pb2 import RegisterPayload
from chores.grpc_generated.users_pb2_grpc import UsersStub


class Test_UsersServer:
    def test_register_user(self, user_service: UsersStub):
        request = RegisterPayload(email="adasd")
        response = user_service.Register(request)