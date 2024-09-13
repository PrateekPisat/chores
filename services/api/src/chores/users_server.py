import time
from concurrent import futures

import grpc
from sqlalchemy import and_
from sqlalchemy.orm import Session

from chores.db import inject_db
from chores.grpc.users_pb2 import (
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
from chores.grpc.users_pb2_grpc import add_UsersServicer_to_server, UsersServicer
from chores.models.user import User

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UsersServer(UsersServicer):
    @inject_db(commit_on_success=True)
    def Register(self, db: Session, request: RegisterPayload, context) -> RegisterResponse:  # noqa: N802
        user = User(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
        )

        db.add(user)
        db.commit()

        return RegisterResponse(user_id=user.id)

    @inject_db(commit_on_success=True)
    def Login(self, db: Session, request: LoginPayload, context) -> LoginResponse:  # noqa: N802
        user = (
            db.query(User)
            .filter(and_(User.email == request.email, User.password == request.password))
            .one_or_none()
        )
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Invalid email or password!")
            return LoginResponse()

        return LoginResponse(user_id=user.id, token="")

    @inject_db(commit_on_success=True)
    def GetUser(self, db: Session, request: GetUserPayload, context) -> GetUserResponse:  # noqa: N802
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

    @inject_db(commit_on_success=True)
    def UpdateUser(self, db: Session, request: UpdateUserPayload, context) -> UpdateUserResponse:  # noqa: N802
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

    @inject_db(commit_on_success=True)
    def DeleteUser(self, db: Session, request: DeleteUserPayload, context) -> DeleteUserResponse:  # noqa: N802
        user = db.query(User).filter(User.id == request.user_id).one_or_none()
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with user id: {request.user_id} not found!")
            return DeleteUserResponse()

        db.delete(user)
        db.commit()

        return DeleteUserResponse(user_id=user.id)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UsersServicer_to_server(UsersServer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
