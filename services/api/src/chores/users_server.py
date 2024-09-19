import time
from concurrent import futures

import grpc
from dependency_injector import providers
from dependency_injector.wiring import inject, Provide
from sqlalchemy import and_
from sqlalchemy.orm import Session

from chores.config import Config, load_config
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
    def Register(
        self, request: RegisterPayload, context, db: Session = Provide[Container.postgres]
    ) -> RegisterResponse:  # noqa: N802
        user = User(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
        )

        import pdb

        pdb.set_trace()
        db.add(user)
        db.commit()

        return RegisterResponse(user_id=user.id)

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
    def UpdateUser(
        self, request: UpdateUserPayload, context, db: Session = Provide[Container.postgres]
    ) -> UpdateUserResponse:  # noqa: N802
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
    def DeleteUser(
        self, request: DeleteUserPayload, context, db: Session = Provide[Container.postgres]
    ) -> DeleteUserResponse:  # noqa: N802
        user = db.query(User).filter(User.id == request.user_id).one_or_none()
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with user id: {request.user_id} not found!")
            return DeleteUserResponse()

        db.delete(user)
        db.commit()

        return DeleteUserResponse(user_id=user.id)


def serve():
    config = load_config()

    container = Container()
    container.config.override(providers.Factory(Config, **config.model_dump()))
    container.init_resources()

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