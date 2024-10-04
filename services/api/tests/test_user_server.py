import uuid

import grpc
import pytest
from chores.grpc_generated.chores_pb2 import (
    DeleteUserPayload,
    DeleteUserResponse,
    GetUserPayload,
    GetUserResponse,
    LoginPayload,
    LoginResponse,
    RegisterPayload,
    SearchUserPayload,
    SearchUserResponse,
    UpdateUserPayload,
    UpdateUserResponse,
)
from chores.grpc_generated.chores_pb2_grpc import UsersStub
from chores.models.user import User
from sqlalchemy.orm import Session

from tests.factories.base import ModelFactory


class Test_UsersServer:
    def test_register_user(self, user_service: UsersStub, db: Session):
        request = RegisterPayload(email="adasd", password="asdasd", first_name="asdasd", last_name="asdasd")
        response = user_service.Register(request)

        assert response.user_id is not None

        user = db.query(User).filter(User.id == response.user_id).one_or_none()
        assert user is not None

        assert user.email == request.email
        assert user.first_name == request.first_name
        assert user.last_name == request.last_name

    def test_login(self, user_service: UsersStub, mf: ModelFactory):
        user = mf.user.user()
        request = LoginPayload(email=user.email, password=user.password)

        response: LoginResponse = user_service.Login(request)

        assert response.user_id == str(user.id)
        assert response.token == ""

    def test_login_invalid(self, user_service: UsersStub):
        request = LoginPayload(email="adasd", password="asdasd")

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            user_service.Login(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND

    def test_get_user(self, user_service: UsersStub, mf: ModelFactory):
        user = mf.user.user()
        request = GetUserPayload(user_id=str(user.id))

        response: GetUserResponse = user_service.GetUser(request)

        assert response.user_id == str(user.id)
        assert response.email == user.email
        assert response.first_name == user.first_name
        assert response.last_name == user.last_name

    def test_get_user_invalid(self, user_service: UsersStub):
        request = GetUserPayload(user_id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            user_service.GetUser(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"User with user id: {request.user_id} not found!"

    def test_update_user(self, user_service: UsersStub, mf: ModelFactory, db: Session):
        user_id = uuid.uuid4()
        mf.user.user(id=user_id)
        request = UpdateUserPayload(user_id=str(user_id), first_name="new first name", last_name="new last name")

        response: UpdateUserResponse = user_service.UpdateUser(request)

        assert response.user_id == str(user_id)

        db.expunge_all()
        user = db.query(User).filter(User.id == user_id).one()
        assert user.first_name == request.first_name
        assert user.last_name == request.last_name

    def test_update_user_invalid(self, user_service: UsersStub):
        request = UpdateUserPayload(user_id=str(uuid.uuid4()), first_name="new first name", last_name="new last name")

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            user_service.UpdateUser(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"User with user id: {request.user_id} not found!"

    def test_delete_user(self, user_service: UsersStub, mf: ModelFactory, db: Session):
        user = mf.user.user()
        request = DeleteUserPayload(user_id=str(user.id))

        response: DeleteUserResponse = user_service.DeleteUser(request)

        assert response.user_id == str(user.id)
        assert db.query(User).filter(User.id == user.id).one_or_none() is None

    def test_delete_user_invalid(self, user_service: UsersStub):
        request = DeleteUserPayload(user_id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            user_service.DeleteUser(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"User with user id: {request.user_id} not found!"

    def test_search_user(self, user_service: UsersStub, mf: ModelFactory):
        user = mf.user.user()
        request = SearchUserPayload(email=user.email)

        response: SearchUserResponse = user_service.SearchUser(request)

        assert len(response.users) == 1
        assert response.users[0].user_id == str(user.id)
        assert response.users[0].email == user.email
        assert response.users[0].first_name == user.first_name
        assert response.users[0].last_name == user.last_name

    @pytest.mark.parametrize("email", ["test", "email", "test@", "@email"])
    def test_search_user_filter(self, user_service: UsersStub, mf: ModelFactory, email: str):
        user = mf.user.user(email="test@email.com")
        request = SearchUserPayload(email=email)

        response: SearchUserResponse = user_service.SearchUser(request)

        assert len(response.users) == 1
        assert response.users[0].user_id == str(user.id)
        assert response.users[0].email == user.email
        assert response.users[0].first_name == user.first_name
        assert response.users[0].last_name == user.last_name

    @pytest.mark.parametrize("query", ["test1", "email", "@email", "1test", "random_name"])
    def test_search_user_no_match(self, user_service: UsersStub, mf: ModelFactory, query: str):
        mf.user.user(email="test@example.com")
        request = SearchUserPayload(email=query)

        response: SearchUserResponse = user_service.SearchUser(request)

        assert len(response.users) == 0
