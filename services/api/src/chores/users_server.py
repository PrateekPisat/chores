import time
from concurrent import futures

import grpc
from dependency_injector.wiring import inject, Provide
from grpc._server import _Context
from sqlalchemy import and_
from sqlalchemy.orm import Session

from chores.deps import Container
from chores.grpc_generated.users_pb2 import (
    DeleteUserPayload,
    DeleteUserResponse,
    GetUserPayload,
    GetUserResponse,
    LoginPayload,
    LoginResponse,
    RegisterPayload,
    RegisterResponse,
    UpdateUserPayload,
    UpdateUserResponse,
)
from chores.grpc_generated.users_pb2_grpc import add_UsersServicer_to_server, UsersServicer
from chores.models.user import User

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UsersServer(UsersServicer):
    @inject
    def Register(  # noqa: N802
        self, request: RegisterPayload, context: _Context, postgres: Session = Provide[Container.postgres]
    ):
        user = User(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
        )
        postgres.add(user)
        postgres.commit()

        return RegisterResponse(user_id=str(user.id))

    @inject
    def Login(self, request: LoginPayload, context, db: Session = Provide[Container.postgres]) -> LoginResponse:  # noqa: N802
        user = db.query(User).filter(and_(User.email == request.email, User.password == request.password)).one_or_none()
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Invalid email or password!")
            return LoginResponse()

        return LoginResponse(user_id=user.id, token="")

    @inject
    def GetUser(self, request: GetUserPayload, context, db: Session = Provide[Container.postgres]) -> GetUserResponse:  # noqa: N802
        user = db.query(User).filter(User.id == request.user_id).one_or_none()
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with user id: {request.user_id} not found!")
            return GetUserResponse()

        return GetUserResponse(
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    @inject
    def UpdateUser(  # noqa: N802
        self, request: UpdateUserPayload, context, db: Session = Provide[Container.postgres]
    ) -> UpdateUserResponse:
        user = db.query(User).filter(User.id == request.user_id).one_or_none()
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with user id: {request.user_id} not found!")
            return UpdateUserResponse()

        user.email = request.email
        user.first_name = request.first_name
        user.last_name = request.last_name

        db.commit()

        return UpdateUserResponse(user_id=user.id)

    @inject
    def DeleteUser(  # noqa: N802
        self, request: DeleteUserPayload, context, db: Session = Provide[Container.postgres]
    ) -> DeleteUserResponse:
        user = db.query(User).filter(User.id == request.user_id).one_or_none()
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with user id: {request.user_id} not found!")
            return DeleteUserResponse()

        db.delete(user)
        db.commit()

        return DeleteUserResponse(user_id=user.id)


def serve():
    container = Container()
    container.init_resources()
    container.inherited_providers()
    container.wire(modules=[__name__])

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UsersServicer_to_server(UsersServer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
