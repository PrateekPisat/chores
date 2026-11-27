import logging
import time
from concurrent import futures

import grpc
from dependency_injector.wiring import inject, Provide
from grpc._server import _Context
from setuplog import log, setup_logging
from sqlalchemy import func

from chores.auth import (
    current_user_email,
    current_user_sub,
    escape_like,
    require_caller,
    require_chore_member,
    require_self,
)
from chores.db import Database
from chores.deps import Container
from chores.errors import InvalidArgument, PermissionDenied, Unauthenticated
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
from chores.interceptors import AuthInterceptor, ExceptionToStatusInterceptor
from chores.models.chore import Chore
from chores.models.house import House, HouseMember
from chores.models.user import User
from chores.utils import get_server_credentials

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UsersServer(UsersServicer):
    @inject
    def GetUser(
        self, request: GetUserPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> GetUserResponse:
        with database.session() as db:
            caller = require_caller(db)
            require_self(caller, request.user_id)
            user = caller

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
            user = require_caller(db)
            require_self(user, request.user_id)

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
            user = require_caller(db)
            require_self(user, request.user_id)

            db.delete(user)
            db.commit()

            return DeleteUserResponse(user_id=str(user.id))

    @inject
    def SearchUser(
        self, request: SearchUserPayload, context: _Context, database: Database = Provide[Container.database]
    ) -> SearchUserResponse:
        with database.session() as db:
            caller = require_caller(db)
            users = db.query(User)
            email = request.email.strip()

            if request.chore_id:
                require_chore_member(db, caller, request.chore_id)
                users = users.join(HouseMember).join(House).join(Chore).filter(Chore.id == request.chore_id)
            elif len(email) < 3:
                return SearchUserResponse(users=[])

            if email:
                users = users.filter(User.email.like(f"%{escape_like(email)}%", escape="\\"))

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
        sub = current_user_sub.get()
        if not sub:
            raise Unauthenticated("Missing token subject")
        if request.sub != sub:
            raise PermissionDenied("Cannot sync another user")

        email = _sync_email(request.email)
        with database.session() as db:
            user = db.query(User).filter(User.sub == sub).one_or_none()
            email_owner = db.query(User).filter(func.lower(User.email) == email).one_or_none()
            if user is None:
                if email_owner is not None:
                    raise PermissionDenied("Email does not match this account")
                if not request.first_name or not request.last_name:
                    raise InvalidArgument("Name is required")
                user = User(
                    email=email,
                    first_name=request.first_name,
                    last_name=request.last_name,
                    sub=sub,
                    picture=request.picture or None,
                    nickname=request.nickname or None,
                )
                db.add(user)
            else:
                if email_owner is not None and email_owner.id != user.id:
                    raise PermissionDenied("Email does not match this account")
                if user.email.lower() != email:
                    raise PermissionDenied("Email does not match this account")
                _apply_profile(user, request)
            db.commit()
            return SyncUserResponse(user=user.as_dict)


def _sync_email(email: str) -> str:
    normalized = email.strip().lower()
    if not normalized:
        raise InvalidArgument("Email is required")

    token_email = current_user_email.get()
    if token_email and normalized != token_email.strip().lower():
        raise PermissionDenied("Email does not match this account")
    return normalized


def _apply_profile(user: User, request: SyncUserPayload) -> None:
    if request.first_name:
        user.first_name = request.first_name
    if request.last_name:
        user.last_name = request.last_name
    if request.picture:
        user.picture = request.picture
    if request.nickname:
        user.nickname = request.nickname


def serve():
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__, ".interceptors"])
    config = container.config()
    setup_logging(
        log_level=logging.getLevelNamesMapping()[config.logging.level.upper()],
        namespace="chores.users_server",
        style=" %(name)s :: %(levelname)-8s :: %(message)s",
    )

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=[ExceptionToStatusInterceptor(), AuthInterceptor()]
    )
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
