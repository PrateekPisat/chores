import uuid

import grpc
import jwt
import pendulum
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
        assert exception.code() == grpc.StatusCode.PERMISSION_DENIED

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

    def test_update_user_invalid(self, user_service: UsersStub, mf: ModelFactory, config: Config):
        user = mf.user.user()
        request = UpdateUserPayload(user_id=str(uuid.uuid4()), first_name="new first name", last_name="new last name")

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            token = get_token_payload(user, config.cryptography.secret_key)
            user_service.UpdateUser(request, metadata=[("authorization", f"Bearer {token}")])

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.PERMISSION_DENIED

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
        assert exception.code() == grpc.StatusCode.PERMISSION_DENIED

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

    def test_search_user_chore_id(self, user_service: UsersStub, mf: ModelFactory, config: Config):
        user = mf.user.user()
        house = mf.house.house()
        chore = mf.chore.chore(house=house)
        mf.house.house_member(house_id=house.id, user_id=user.id)
        request = SearchUserPayload(chore_id=str(chore.id))

        token = get_token_payload(user, config.cryptography.secret_key)
        response: SearchUserResponse = user_service.SearchUser(request, metadata=[("authorization", f"Bearer {token}")])

        assert len(response.users) == 1
        assert response.users[0].user_id == str(user.id)

    @pytest.mark.parametrize("query", ["test1", "email", "@email", "1test", "random_name"])
    def test_search_user_no_match(self, user_service: UsersStub, mf: ModelFactory, config: Config, query: str):
        user = mf.user.user(email="test@example.com")
        token = get_token_payload(user, config.cryptography.secret_key)
        request = SearchUserPayload(email=query)

        response: SearchUserResponse = user_service.SearchUser(request, metadata=[("authorization", f"Bearer {token}")])

        assert len(response.users) == 0

    def test_search_user_empty_query_returns_nobody(self, user_service: UsersStub, mf: ModelFactory, config: Config):
        mf.user.user(email="hidden@example.com")
        caller = mf.user.user(email="caller@example.com")
        token = get_token_payload(caller, config.cryptography.secret_key)

        response = user_service.SearchUser(SearchUserPayload(), metadata=[("authorization", f"Bearer {token}")])
        wildcard = user_service.SearchUser(
            SearchUserPayload(email="%"), metadata=[("authorization", f"Bearer {token}")]
        )

        assert len(response.users) == 0
        assert len(wildcard.users) == 0

    def test_it_syncs_new_user(self, user_service: UsersStub, db: Session, config: Config):
        payload = SyncUserPayload(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            sub=fake.md5(),
            picture=fake.image_url(),
            nickname=fake.user_name(),
        )
        token = jwt.encode(
            {"sub": payload.sub, "exp": pendulum.now().add(days=1).timestamp()},
            config.cryptography.secret_key,
        )

        user_service.SyncUser(payload, metadata=[("authorization", f"Bearer {token}")])

        users = db.query(User).all()
        assert len(users) == 1

        assert users[0].email == payload.email.lower()
        assert users[0].first_name == payload.first_name
        assert users[0].last_name == payload.last_name
        assert users[0].sub == payload.sub
        assert users[0].picture == payload.picture
        assert users[0].nickname == payload.nickname

    def test_it_rejects_sync_for_another_subject(self, user_service: UsersStub, config: Config):
        payload = SyncUserPayload(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            sub="victim-subject",
            picture=fake.image_url(),
            nickname=fake.user_name(),
        )
        token = jwt.encode(
            {"sub": "attacker-subject", "exp": pendulum.now().add(days=1).timestamp()},
            config.cryptography.secret_key,
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            user_service.SyncUser(payload, metadata=[("authorization", f"Bearer {token}")])

        assert e.value.code() == grpc.StatusCode.PERMISSION_DENIED

    def test_it_rejects_sync_when_email_belongs_to_someone_else(
        self, user_service: UsersStub, mf: ModelFactory, db: Session, config: Config
    ):
        owner = mf.user.user(email="owner@example.com")
        payload = SyncUserPayload(
            email=owner.email,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            sub="new-subject",
            picture=fake.image_url(),
            nickname=fake.user_name(),
        )
        token = jwt.encode(
            {"sub": payload.sub, "exp": pendulum.now().add(days=1).timestamp()},
            config.cryptography.secret_key,
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            user_service.SyncUser(payload, metadata=[("authorization", f"Bearer {token}")])

        assert e.value.code() == grpc.StatusCode.PERMISSION_DENIED
        assert db.query(User).filter(User.sub == payload.sub).one_or_none() is None

    def test_it_rejects_sync_when_email_changes(
        self, user_service: UsersStub, mf: ModelFactory, db: Session, config: Config
    ):
        user = mf.user.user(email="kept@example.com", first_name="Kept")
        payload = SyncUserPayload(
            email="other@example.com",
            first_name="Changed",
            last_name=user.last_name,
            sub=user.sub,
            picture=user.picture,
            nickname=user.nickname,
        )
        token = jwt.encode(
            {"sub": user.sub, "exp": pendulum.now().add(days=1).timestamp()},
            config.cryptography.secret_key,
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            user_service.SyncUser(payload, metadata=[("authorization", f"Bearer {token}")])

        assert e.value.code() == grpc.StatusCode.PERMISSION_DENIED
        db.expunge_all()
        stored = db.query(User).filter(User.id == user.id).one()
        assert stored.email == "kept@example.com"
        assert stored.first_name == "Kept"

    def test_it_rejects_sync_when_body_email_differs_from_token(self, user_service: UsersStub, config: Config):
        payload = SyncUserPayload(
            email="body@example.com",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            sub="subject-1",
            picture=fake.image_url(),
            nickname=fake.user_name(),
        )
        token = jwt.encode(
            {"sub": payload.sub, "email": "token@example.com", "exp": pendulum.now().add(days=1).timestamp()},
            config.cryptography.secret_key,
        )

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            user_service.SyncUser(payload, metadata=[("authorization", f"Bearer {token}")])

        assert e.value.code() == grpc.StatusCode.PERMISSION_DENIED

    def test_it_updates_profile_when_email_matches(
        self, user_service: UsersStub, mf: ModelFactory, db: Session, config: Config
    ):
        user = mf.user.user(email="same@example.com", first_name="Old")
        payload = SyncUserPayload(
            email="Same@example.com",
            first_name="New",
            last_name="Name",
            sub=user.sub,
            picture="https://example.com/picture.png",
            nickname="newnick",
        )
        token = jwt.encode(
            {"sub": user.sub, "email": "same@example.com", "exp": pendulum.now().add(days=1).timestamp()},
            config.cryptography.secret_key,
        )

        user_service.SyncUser(payload, metadata=[("authorization", f"Bearer {token}")])

        db.expunge_all()
        stored = db.query(User).filter(User.id == user.id).one()
        assert stored.email == "same@example.com"
        assert stored.first_name == "New"
        assert stored.last_name == "Name"
        assert stored.picture == payload.picture
        assert stored.nickname == payload.nickname
