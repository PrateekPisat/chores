import uuid

import grpc
import pytest
from chores.config import Config
from chores.grpc_generated.chores_pb2 import (
    AddMembersPayload,
    CreatePayload,
    DeletePayload,
    GetPayload,
    HouseResponse,
    ListHousePayload,
    RemoveMemberPayload,
    SearchHousePayload,
    UpdatePayload,
)
from chores.grpc_generated.chores_pb2_grpc import HouseStub
from chores.models.house import House, HouseMember
from chores.utils import get_token_payload
from sqlalchemy.orm import Session

from tests.factories.base import ModelFactory


class Test_HouseServer:
    def test_it_creates_a_house(self, house_service: HouseStub, db: Session, mf: ModelFactory, config: Config):
        user = mf.user.user(email="test@example.com")
        request = CreatePayload(name="House 1")

        token = get_token_payload(user, config.cryptography.secret_key)
        response = house_service.Create(request, metadata=(("authorization", f"Bearer {token}"),))
        assert response.house_id

        house = db.query(House).filter(House.id == response.house_id).one_or_none()
        assert house
        assert house.name == request.name
        assert str(house.id) == response.house_id
        member = db.query(HouseMember).filter(HouseMember.house_id == house.id).one()
        assert member.user_id == user.id

    def test_it_lists_houses(self, house_service: HouseStub, db: Session, mf: ModelFactory, config: Config):
        user = mf.user.user(email="test@example.com")
        house = mf.house.house()
        mf.house.house_member(house_id=house.id, user_id=user.id)
        request = ListHousePayload(user_id=str(user.id))

        token = get_token_payload(user, config.cryptography.secret_key)
        response = house_service.ListHouses(request, metadata=(("authorization", f"Bearer {token}"),))

        assert len(response.houses) == 1
        assert response.houses == [HouseResponse(house_id=str(house.id), name=house.name)]

    @pytest.mark.parametrize("name", ["House 1", "House", "Hou", "house 1"])
    def test_it_searches_houses_by_name(self, house_service: HouseStub, mf: ModelFactory, config: Config, name: str):
        user = mf.user.user(email="test@example.com")
        house = mf.house.house(name="House 1")
        mf.house.house_member(house_id=house.id, user_id=user.id)
        request = SearchHousePayload(name=name)

        token = get_token_payload(user, config.cryptography.secret_key)
        response = house_service.SearchHouse(request, metadata=(("authorization", f"Bearer {token}"),))

        assert len(response.houses) == 1
        assert response.houses == [HouseResponse(house_id=str(house.id), name=house.name)]

    def test_it_gets_a_house(self, house_service: HouseStub, db: Session, mf: ModelFactory, config: Config):
        user = mf.user.user(email="test@example.com")
        house = mf.house.house()
        mf.house.house_member(house_id=house.id, user_id=user.id)
        request = GetPayload(house_id=str(house.id))

        token = get_token_payload(user, config.cryptography.secret_key)
        response = house_service.Get(request, metadata=(("authorization", f"Bearer {token}"),))
        assert response.house_id == str(house.id)
        assert response.name == house.name

    def test_it_get_house_not_found(self, house_service: HouseStub, mf: ModelFactory, config: Config):
        user = mf.user.user(email="test@example.com")
        request = GetPayload(house_id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            token = get_token_payload(user, config.cryptography.secret_key)
            house_service.Get(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND

    def test_it_updates_a_house(self, house_service: HouseStub, db: Session, mf: ModelFactory, config: Config):
        user = mf.user.user(email="test@example.com")
        house = mf.house.house()
        mf.house.house_member(house_id=house.id, user_id=user.id)
        request = UpdatePayload(name="House 2", house_id=str(house.id))

        token = get_token_payload(user, config.cryptography.secret_key)
        response = house_service.Update(request, metadata=(("authorization", f"Bearer {token}"),))
        assert response.house_id == str(house.id)

        house = db.query(House).filter(House.id == house.id).one_or_none()
        assert house.name == request.name

    def test_it_updates_house_not_found(self, house_service: HouseStub, mf: ModelFactory, config: Config):
        user = mf.user.user(email="test@example.com")
        request = UpdatePayload(name="House 2", house_id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            token = get_token_payload(user, config.cryptography.secret_key)
            house_service.Update(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == "House not found!"

    def test_it_deletes_a_house(self, house_service: HouseStub, db: Session, mf: ModelFactory, config: Config):
        user = mf.user.user(email="test@example.com")
        house = mf.house.house()
        mf.house.house_member(house_id=house.id, user_id=user.id)
        request = DeletePayload(house_id=str(house.id))

        token = get_token_payload(user, config.cryptography.secret_key)
        response = house_service.Delete(request, metadata=(("authorization", f"Bearer {token}"),))
        assert response.house_id == str(house.id)

        db.expunge_all()
        members = db.query(HouseMember).filter(HouseMember.house_id == house.id).all()
        house = db.query(House).filter(House.id == house.id).one_or_none()
        assert house is None
        assert len(members) == 0

    def test_it_deletes_house_not_found(self, house_service: HouseStub, mf: ModelFactory, config: Config):
        user = mf.user.user(email="test@example.com")
        request = DeletePayload(house_id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            token = get_token_payload(user, config.cryptography.secret_key)
            house_service.Delete(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == "House not found!"

    def test_it_adds_members_to_house(self, house_service: HouseStub, db: Session, mf: ModelFactory, config: Config):
        user = mf.user.user(email="test@example.com")
        house = mf.house.house()
        mf.house.house_member(house_id=house.id, user_id=user.id)
        user1 = mf.user.user()
        user2 = mf.user.user()
        request = AddMembersPayload(house_id=str(house.id), user_ids=[str(user1.id), str(user2.id)])

        token = get_token_payload(user, config.cryptography.secret_key)
        response = house_service.AddMembers(request, metadata=(("authorization", f"Bearer {token}"),))
        assert response.house_id == str(house.id)
        assert response.user_ids == [str(user1.id), str(user2.id)]

        db.expunge_all()
        members = db.query(HouseMember).filter(HouseMember.house_id == house.id).all()
        assert {member.user_id for member in members} == {user.id, user1.id, user2.id}

    def test_it_adds_members_to_house_not_found(self, house_service: HouseStub, mf: ModelFactory, config: Config):
        user = mf.user.user(email="test@example.com")
        user = mf.user.user()
        request = AddMembersPayload(house_id=str(uuid.uuid4()), user_ids=[str(user.id)])

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            token = get_token_payload(user, config.cryptography.secret_key)
            house_service.AddMembers(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == "House not found!"

    def test_it_adds_members_to_house_user_not_found(self, house_service: HouseStub, mf: ModelFactory, config: Config):
        user = mf.user.user(email="test@example.com")
        house = mf.house.house()
        mf.house.house_member(house_id=house.id, user_id=user.id)
        user_id = uuid.uuid4()
        request = AddMembersPayload(house_id=str(house.id), user_ids=[str(user_id)])

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            token = get_token_payload(user, config.cryptography.secret_key)
            house_service.AddMembers(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == "User not found!"

    def test_it_adds_members_to_house_user_already_exists(
        self, house_service: HouseStub, mf: ModelFactory, config: Config
    ):
        owner = mf.user.user(email="test@example.com")
        house = mf.house.house()
        mf.house.house_member(house_id=house.id, user_id=owner.id)
        member = mf.user.user()
        request = AddMembersPayload(house_id=str(house.id), user_ids=[str(member.id)])

        token = get_token_payload(owner, config.cryptography.secret_key)
        house_service.AddMembers(request, metadata=(("authorization", f"Bearer {token}"),))
        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            house_service.AddMembers(request, metadata=(("authorization", f"Bearer {token}"),))

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.ALREADY_EXISTS
        assert exception.details() == f"User {member.id} already exists in the house {house.id}!"

    def test_it_removes_member(self, house_service: HouseStub, mf: ModelFactory, config: Config):
        owner = mf.user.user(email="test@example.com")
        house = mf.house.house()
        mf.house.house_member(house_id=house.id, user_id=owner.id)
        member = mf.user.user()
        request = RemoveMemberPayload(house_id=str(house.id), user_id=str(member.id))

        token = get_token_payload(owner, config.cryptography.secret_key)
        response = house_service.RemoveMember(request, metadata=(("authorization", f"Bearer {token}"),))
        assert response.house_id == str(house.id)
        assert response.user_id == str(member.id)

    def test_it_gets_members(self, house_service: HouseStub, mf: ModelFactory, config: Config):
        user = mf.user.user(email="test@example.com")
        house = mf.house.house()
        user = mf.user.user()
        mf.house.house_member(house_id=house.id, user_id=user.id)

        request = GetPayload(house_id=str(house.id))
        token = get_token_payload(user, config.cryptography.secret_key)
        response = house_service.GetMembers(request, metadata=(("authorization", f"Bearer {token}"),))

        assert response.house_id == str(house.id)
        assert len(response.users) == 1
        assert response.users[0].id == str(user.id)
        assert response.users[0].first_name == user.first_name
        assert response.users[0].last_name == user.last_name
        assert response.users[0].email == user.email

    def test_it_does_not_get_another_users_house(self, house_service: HouseStub, mf: ModelFactory, config: Config):
        owner = mf.user.user()
        stranger = mf.user.user()
        house = mf.house.house()
        mf.house.house_member(house_id=house.id, user_id=owner.id)
        request = GetPayload(house_id=str(house.id))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            token = get_token_payload(stranger, config.cryptography.secret_key)
            house_service.Get(request, metadata=(("authorization", f"Bearer {token}"),))

        assert e.value.code() == grpc.StatusCode.PERMISSION_DENIED
