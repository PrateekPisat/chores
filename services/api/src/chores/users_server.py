import time
from concurrent import futures

import grpc
from dependency_injector.wiring import inject, Provide
from grpc._server import _Context
from pydantic import ValidationError
from setuplog import log, setup_logging
from sqlalchemy import and_

from chores.db import Database
from chores.deps import Container
from chores.errors import NotFound
from chores.grpc_generated.chores_pb2 import (
    DeleteUserPayload,
    DeleteUserResponse,
    GetUserPayload,
    GetUserResponse,
    LoginPayload,
    LoginResponse,
    RegisterErrorResponse,
    RegisterPayload,
    RegisterResponse,
    SearchUserPayload,
    SearchUserResponse,
    UpdateUserPayload,
    UpdateUserResponse,
)
from chores.grpc_generated.chores_pb2_grpc import add_UsersServicer_to_server, UsersServicer
from chores.interceptors import ExceptionToStatusInterceptor
from chores.models.user import User
from chores.schema import RegisterUserPayload
from chores.utils import get_token_payload, parse_errors

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UsersServer(UsersServicer):
    def ValidateRegisterPayload(self, request: RegisterPayload, context: _Context) -> RegisterErrorResponse:
        try:
            RegisterUserPayload(
                email=request.email,
                password=request.password,
                confirm_password=request.confirm_password,
                first_name=request.first_name,
                last_name=request.last_name,
            )
        except ValidationError as e:
            return RegisterErrorResponse(**parse_errors(e))

        return RegisterErrorResponse()

    @inject
    def Register(
        self,
        request: RegisterPayload,
        context: _Context,
        database: Database = Provide[Container.database],
        config=Provide[Container.config],
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

            token = get_token_payload(user, config.cryptography.secret_key)
            return RegisterResponse(user_id=str(user.id), token=token)

    @inject
    def Login(
        self,
        request: LoginPayload,
        context: _Context,
        database: Database = Provide[Container.database],
        config=Provide[Container.config],
    ) -> LoginResponse:
        with database.session() as db:
            user = (
                db.query(User)
                .filter(and_(User.email == request.email, User.password == request.password))
                .one_or_none()
            )
        if not user:
            raise NotFound(details="Invalid email or password!")

        token = get_token_payload(user, config.cryptography.secret_key)
        return LoginResponse(user_id=str(user.id), token=token)

    @inject
    def GetUser(
        self, request: GetUserPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> GetUserResponse:
        with database.session() as db:
            user = db.query(User).filter(User.id == request.user_id).one_or_none()
        if not user:
            raise NotFound(details=f"User with user id: {request.user_id} not found!")

        return GetUserResponse(
            user_id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    @inject
    def UpdateUser(
        self, request: UpdateUserPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> UpdateUserResponse:
        with database.session() as db:
            user = db.query(User).filter(User.id == request.user_id).one_or_none()
            if not user:
                raise NotFound(details=f"User with user id: {request.user_id} not found!")

            user.email = request.email
            user.first_name = request.first_name
            user.last_name = request.last_name
            db.add(user)
            db.commit()

            return UpdateUserResponse(user_id=str(user.id))

    @inject
    def DeleteUser(
        self, request: DeleteUserPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> DeleteUserResponse:
        with database.session() as db:
            user = db.query(User).filter(User.id == request.user_id).one_or_none()
            if not user:
                raise NotFound(details=f"User with user id: {request.user_id} not found!")

            db.delete(user)
            db.commit()

            return DeleteUserResponse(user_id=str(user.id))

    @inject
    def SearchUser(
        self, request: SearchUserPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> SearchUserResponse:
        with database.session() as db:
            users = db.query(User).filter(User.email.like(f"%{request.email}%")).all()

        return SearchUserResponse(
            users=[
                GetUserResponse(
                    user_id=str(user.id), email=user.email, first_name=user.first_name, last_name=user.last_name
                )
                for user in users
            ]
        )


def serve():
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    config = container.config()
    setup_logging(
        log_level=config.logging.level,
        namespace="chores.users_server",
        style=" %(name)s :: %(levelname)-8s :: %(message)s",
    )

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[ExceptionToStatusInterceptor()])
    add_UsersServicer_to_server(UsersServer(), server)
    server.add_insecure_port(f"[::]:{config.user_service_port}")
    server.start()
    log.info("Users server started on port %s", config.user_service_port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
