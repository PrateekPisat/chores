import uuid

import grpc
import jwt
import pytest
from argon2 import PasswordHasher
from chores.config import Config
from chores.grpc_generated.chores_pb2 import (
    DeleteUserPayload,
    DeleteUserResponse,
    GetUserPayload,
    GetUserResponse,
    LoginPayload,
    LoginResponse,
    LogoutPayload,
    LogoutResponse,
    RegisterPayload,
    SearchUserPayload,
    SearchUserResponse,
    UpdateUserPayload,
    UpdateUserResponse,
)
from chores.grpc_generated.chores_pb2_grpc import UsersStub
from chores.models.user import TokenBlacklist, User
from chores.utils import get_token_payload
from sqlalchemy.orm import Session

from tests.factories.base import ModelFactory


class Test_UsersServer:
    def test_register_user(self, user_service: UsersStub, db: Session, config: Config):
        request = RegisterPayload(email="adasd", password="asdasd", first_name="asdasd", last_name="asdasd")
        response = user_service.Register(request)

        assert response.user_id is not None

        user = db.query(User).filter(User.id == response.user_id).one_or_none()
        assert user is not None

        token_payload = jwt.decode(response.token, config.cryptography.secret_key, algorithms=["HS256"])
        assert user.email == request.email
        assert user.first_name == request.first_name
        assert user.last_name == request.last_name
        assert response.user_id == str(user.id)
        assert token_payload["sub"] == str(user.id)
        assert token_payload["name"] == user.name
        assert token_payload["nickname"] == user.first_name

    def test_login(self, user_service: UsersStub, mf: ModelFactory, config: Config, password_hasher: PasswordHasher):
        user = mf.user.user(password=password_hasher.hash("password"))
        request = LoginPayload(email=user.email, password="password")

        response: LoginResponse = user_service.Login(request)

        token_payload = jwt.decode(response.token, config.cryptography.secret_key, algorithms=["HS256"])
        assert response.user_id == str(user.id)
        assert token_payload["sub"] == str(user.id)
        assert token_payload["name"] == user.name
        assert token_payload["nickname"] == user.first_name

    def test_login_invalid(self, user_service: UsersStub):
        request = LoginPayload(email="adasd", password="asdasd")

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            user_service.Login(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND

    def test_logout(self, user_service: UsersStub, mf: ModelFactory, db: Session, config: Config):
        user = mf.user.user()
        token = get_token_payload(user, config.cryptography.secret_key)
        request = LogoutPayload(user_id=str(user.id), token=token)

        response: LogoutResponse = user_service.Logout(request, metadata=[("authorization", f"Bearer {token}")])

        assert response.user_id == str(user.id)
        blacklist = db.query(TokenBlacklist).all()
        assert len(blacklist) == 1
        assert blacklist[0].token == token

    def test_logout_user_not_found(self, user_service: UsersStub, mf: ModelFactory, config: Config):
        user = mf.user.user()
        token = get_token_payload(user, config.cryptography.secret_key)

        request = LogoutPayload(user_id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            user_service.Logout(request, metadata=[("authorization", f"Bearer {token}")])

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"User with user id: {request.user_id} not found!"

    def test_get_user(self, user_service: UsersStub, mf: ModelFactory, config: Config):
        user = mf.user.user()
        request = GetUserPayload(user_id=str(user.id))

        token = get_token_payload(user, config.cryptography.secret_key)
        response: GetUserResponse = user_service.GetUser(request, metadata=[("authorization", f"Bearer {token}")])

        assert response.user_id == str(user.id)
        assert response.email == user.email
        assert response.first_name == user.first_name
        assert response.last_name == user.last_name

    def test_get_user_invalid(self, user_service: UsersStub, mf: ModelFactory, config: Config):
        user = mf.user.user()
        request = GetUserPayload(user_id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            token = get_token_payload(user, config.cryptography.secret_key)
            user_service.GetUser(request, metadata=[("authorization", f"Bearer {token}")])

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"User with user id: {request.user_id} not found!"

    def test_update_user(self, user_service: UsersStub, mf: ModelFactory, db: Session, config: Config):
        user_id = uuid.uuid4()
        user = mf.user.user(id=user_id)
        request = UpdateUserPayload(user_id=str(user_id), first_name="new first name", last_name="new last name")

        token = get_token_payload(user, config.cryptography.secret_key)
        response: UpdateUserResponse = user_service.UpdateUser(request, metadata=[("authorization", f"Bearer {token}")])

        assert response.user_id == str(user_id)

        db.expunge_all()
        user = db.query(User).filter(User.id == user_id).one()
        assert user.first_name == request.first_name
        assert user.last_name == request.last_name

    def test_update_user_invalid(self, user_service: UsersStub, config: Config):
        user = User(id=uuid.uuid4())
        request = UpdateUserPayload(user_id=str(uuid.uuid4()), first_name="new first name", last_name="new last name")

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            token = get_token_payload(user, config.cryptography.secret_key)
            user_service.UpdateUser(request, metadata=[("authorization", f"Bearer {token}")])

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"User with user id: {request.user_id} not found!"

    def test_delete_user(self, user_service: UsersStub, mf: ModelFactory, db: Session, config: Config):
        user = mf.user.user()
        request = DeleteUserPayload(user_id=str(user.id))

        token = get_token_payload(user, config.cryptography.secret_key)
        response: DeleteUserResponse = user_service.DeleteUser(request, metadata=[("authorization", f"Bearer {token}")])

        assert response.user_id == str(user.id)
        assert db.query(User).filter(User.id == user.id).one_or_none() is None

    def test_delete_user_invalid(self, user_service: UsersStub, mf: ModelFactory, config: Config):
        user = mf.user.user()
        request = DeleteUserPayload(user_id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            token = get_token_payload(user, config.cryptography.secret_key)
            user_service.DeleteUser(request, metadata=[("authorization", f"Bearer {token}")])

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == f"User with user id: {request.user_id} not found!"

    def test_search_user(self, user_service: UsersStub, mf: ModelFactory, config: Config):
        user = mf.user.user()
        request = SearchUserPayload(email=user.email)

        token = get_token_payload(user, config.cryptography.secret_key)
        response: SearchUserResponse = user_service.SearchUser(request, metadata=[("authorization", f"Bearer {token}")])

        assert len(response.users) == 1
        assert response.users[0].user_id == str(user.id)
        assert response.users[0].email == user.email
        assert response.users[0].first_name == user.first_name
        assert response.users[0].last_name == user.last_name

    @pytest.mark.parametrize("email", ["test", "email", "test@", "@email"])
    def test_search_user_filter(self, user_service: UsersStub, mf: ModelFactory, email: str, config: Config):
        user = mf.user.user(email="test@email.com")
        request = SearchUserPayload(email=email)

        token = get_token_payload(user, config.cryptography.secret_key)
        response: SearchUserResponse = user_service.SearchUser(request, metadata=[("authorization", f"Bearer {token}")])

        assert len(response.users) == 1
        assert response.users[0].user_id == str(user.id)
        assert response.users[0].email == user.email
        assert response.users[0].first_name == user.first_name
        assert response.users[0].last_name == user.last_name

    @pytest.mark.parametrize("query", ["test1", "email", "@email", "1test", "random_name"])
    def test_search_user_no_match(self, user_service: UsersStub, mf: ModelFactory, config: Config, query: str):
        user = mf.user.user(email="test@example.com")
        token = get_token_payload(user, config.cryptography.secret_key)
        request = SearchUserPayload(email=query)

        response: SearchUserResponse = user_service.SearchUser(request, metadata=[("authorization", f"Bearer {token}")])

        assert len(response.users) == 0
