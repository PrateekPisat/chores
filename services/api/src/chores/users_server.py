import time
from concurrent import futures

import grpc
from dependency_injector.wiring import inject, Provide
from grpc._server import _Context
from sqlalchemy import and_

from chores.db import Database
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
        self, request: RegisterPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> RegisterResponse:
        user = User(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
        )
        with database.session() as postgres:
            postgres.add(user)
            postgres.commit()

            return RegisterResponse(user_id=str(user.id))

    @inject
    def Login(self, request: LoginPayload, context, database: Database = Provide[Container.database]) -> LoginResponse:  # noqa: N802
        with database.session() as db:
            user = (
                db.query(User)
                .filter(and_(User.email == request.email, User.password == request.password))
                .one_or_none()
            )
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Invalid email or password!")
            return LoginResponse()

        return LoginResponse(user_id=str(user.id), token="")

    @inject
    def GetUser(  # noqa: N802
        self, request: GetUserPayload, context, database: Database = Provide[Container.database]
    ) -> GetUserResponse:
        with database.session() as db:
            user = db.query(User).filter(User.id == request.user_id).one_or_none()
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with user id: {request.user_id} not found!")
            return GetUserResponse()

        return GetUserResponse(
            user_id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    @inject
    def UpdateUser(  # noqa: N802
        self, request: UpdateUserPayload, context, database: Database = Provide[Container.database]
    ) -> UpdateUserResponse:
        with database.session() as db:
            user = db.query(User).filter(User.id == request.user_id).one_or_none()
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User with user id: {request.user_id} not found!")
                return UpdateUserResponse()

            user.email = request.email
            user.first_name = request.first_name
            user.last_name = request.last_name
            db.add(user)
            db.commit()

            return UpdateUserResponse(user_id=str(user.id))

    @inject
    def DeleteUser(  # noqa: N802
        self, request: DeleteUserPayload, context, database: Database = Provide[Container.database]
    ) -> DeleteUserResponse:
        with database.session() as db:
            user = db.query(User).filter(User.id == request.user_id).one_or_none()
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User with user id: {request.user_id} not found!")
                return DeleteUserResponse()

            db.delete(user)
            db.commit()

            return DeleteUserResponse(user_id=str(user.id))


def serve():
    container = Container()
    container.init_resources()
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
