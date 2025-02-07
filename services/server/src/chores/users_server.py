import time
from concurrent import futures

import grpc
from dependency_injector.wiring import inject, Provide
from grpc._server import _Context
from setuplog import log, setup_logging

from chores.db import Database
from chores.deps import Container
from chores.errors import NotFound
from chores.grpc_generated.chores_pb2 import (
    DeleteUserPayload,
    DeleteUserResponse,
    GetUserPayload,
    GetUserResponse,
    SearchUserPayload,
    SearchUserResponse,
    SyncUserPayload,
    SyncUserResponse,
    UpdateUserPayload,
    UpdateUserResponse,
)
from chores.grpc_generated.chores_pb2_grpc import add_UsersServicer_to_server, UsersServicer
from chores.interceptors import ExceptionToStatusInterceptor
from chores.models.user import User
from chores.utils import get_server_credentials

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UsersServer(UsersServicer):
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
            picture=user.picture,
            nickname=user.nickname,
            sub=user.sub,
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
                    user_id=str(user.id),
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    picture=user.picture,
                    nickname=user.nickname,
                    sub=user.sub,
                )
                for user in users
            ]
        )

    @inject
    def SyncUser(
        self, request: SyncUserPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> SyncUserResponse:
        with database.session() as db:
            user = db.query(User).filter(User.sub == request.sub).one_or_none()
            if not user:
                user = User(
                    email=request.email,
                    first_name=request.first_name,
                    last_name=request.last_name,
                    sub=request.sub,
                    picture=request.picture,
                    nickname=request.nickname,
                )
                db.add(user)
            else:
                user.email = request.email
                user.first_name = request.first_name
                user.last_name = request.last_name
                user.picture = request.picture
                user.nickname = request.nickname

            db.commit()
            return SyncUserResponse(user=user.as_dict)


def serve():
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__, ".interceptors"])
    config = container.config()
    setup_logging(
        log_level=config.logging.level,
        namespace="chores.users_server",
        style=" %(name)s :: %(levelname)-8s :: %(message)s",
    )

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[ExceptionToStatusInterceptor()])
    add_UsersServicer_to_server(UsersServer(), server)
    server.add_secure_port(f"[::]:{config.user_service_port}", get_server_credentials(config))
    server.start()
    log.info("Users server started on port %s", config.user_service_port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
