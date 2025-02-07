import uuid

import grpc
import pytest
from chores.config import Config
from chores.grpc_generated.chores_pb2 import (
    DeleteUserPayload,
    DeleteUserResponse,
    GetUserPayload,
    GetUserResponse,
    SearchUserPayload,
    SearchUserResponse,
    SyncUserPayload,
    UpdateUserPayload,
    UpdateUserResponse,
)
from chores.grpc_generated.chores_pb2_grpc import UsersStub
from chores.models.user import User
from chores.utils import get_token_payload
from faker import Faker
from sqlalchemy.orm import Session

from tests.factories.base import ModelFactory

fake = Faker()


class Test_UsersServer:
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
        assert response.users[0].sub == user.sub
        assert response.users[0].picture == user.picture
        assert response.users[0].nickname == user.nickname

    @pytest.mark.parametrize("query", ["test1", "email", "@email", "1test", "random_name"])
    def test_search_user_no_match(self, user_service: UsersStub, mf: ModelFactory, config: Config, query: str):
        user = mf.user.user(email="test@example.com")
        token = get_token_payload(user, config.cryptography.secret_key)
        request = SearchUserPayload(email=query)

        response: SearchUserResponse = user_service.SearchUser(request, metadata=[("authorization", f"Bearer {token}")])

        assert len(response.users) == 0

    def test_it_syncs_new_user(self, user_service: UsersStub, db: Session):
        payload = SyncUserPayload(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            sub=fake.md5(),
            picture=fake.image_url(),
            nickname=fake.user_name(),
        )

        user_service.SyncUser(payload)

        users = db.query(User).all()
        assert len(users) == 1

        assert users[0].email == payload.email
        assert users[0].first_name == payload.first_name
        assert users[0].last_name == payload.last_name
        assert users[0].sub == payload.sub
        assert users[0].picture == payload.picture
        assert users[0].nickname == payload.nickname

    def test_it_syncs_existing_user(self, user_service: UsersStub, mf: ModelFactory, db: Session):
        user = mf.user.user()
        payload = SyncUserPayload(
            email=user.email,
            first_name="new first name",
            last_name="new last name",
            sub=user.sub,
            picture=user.picture,
            nickname="new nickname",
        )

        user_service.SyncUser(payload)

        users = db.query(User).all()
        assert len(users) == 1

        assert users[0].email == payload.email
        assert users[0].first_name == payload.first_name
        assert users[0].last_name == payload.last_name
        assert users[0].sub == payload.sub
        assert users[0].picture == payload.picture
        assert users[0].nickname == payload.nickname
