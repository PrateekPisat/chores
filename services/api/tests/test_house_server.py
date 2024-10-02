import uuid

import grpc
import pytest
from chores.grpc_generated.house_pb2 import (
    AddMembersPayload,
    CreatePayload,
    DeletePayload,
    GetPayload,
    RemoveMemberPayload,
    UpdatePayload,
)
from chores.grpc_generated.house_pb2_grpc import HouseStub
from chores.models.house import House, HouseMember
from sqlalchemy.orm import Session

from tests.factories.base import ModelFactory


class Test_HouseServer:
    def test_it_creates_a_house(self, house_service: HouseStub, db: Session):
        request = CreatePayload(name="House 1")

        response = house_service.Create(request)
        assert response.house_id

        house = db.query(House).filter(House.id == response.house_id).one_or_none()
        assert house
        assert house.name == request.name
        assert str(house.id) == response.house_id

    def test_it_gets_a_house(self, house_service: HouseStub, db: Session, mf: ModelFactory):
        house = mf.house.house()
        request = GetPayload(house_id=str(house.id))

        response = house_service.Get(request)
        assert response.house_id == str(house.id)
        assert response.name == house.name

    def test_it_get_house_not_found(self, house_service: HouseStub):
        request = GetPayload(house_id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            house_service.Get(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND

    def test_it_updates_a_house(self, house_service: HouseStub, db: Session, mf: ModelFactory):
        house = mf.house.house()
        request = UpdatePayload(name="House 2", house_id=str(house.id))

        response = house_service.Update(request)
        assert response.house_id == str(house.id)

        house = db.query(House).filter(House.id == house.id).one_or_none()
        assert house.name == request.name

    def test_it_updates_house_not_found(self, house_service: HouseStub):
        request = UpdatePayload(name="House 2", house_id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            house_service.Update(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == "House not found!"

    def test_it_deletes_a_house(self, house_service: HouseStub, db: Session, mf: ModelFactory):
        house = mf.house.house()
        request = DeletePayload(house_id=str(house.id))

        response = house_service.Delete(request)
        assert response.house_id == str(house.id)

        db.expunge_all()
        house = db.query(House).filter(House.id == house.id).one_or_none()
        assert house is None

    def test_it_deletes_house_not_found(self, house_service: HouseStub):
        request = DeletePayload(house_id=str(uuid.uuid4()))

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            house_service.Delete(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == "House not found!"

    def test_it_adds_members_to_house(self, house_service: HouseStub, db: Session, mf: ModelFactory):
        house = mf.house.house()
        user1 = mf.user.user()
        user2 = mf.user.user()
        request = AddMembersPayload(house_id=str(house.id), user_ids=[str(user1.id), str(user2.id)])

        response = house_service.AddMembers(request)
        assert response.house_id == str(house.id)
        assert response.user_ids == [str(user1.id), str(user2.id)]

        db.expunge_all()
        members = db.query(HouseMember).filter(HouseMember.house_id == house.id).all()
        assert len(members) == 2
        assert members[0].user_id == user1.id
        assert members[0].house_id == house.id
        assert members[1].user_id == user2.id

    def test_it_adds_members_to_house_not_found(self, house_service: HouseStub, mf: ModelFactory):
        user = mf.user.user()
        request = AddMembersPayload(house_id=str(uuid.uuid4()), user_ids=[str(user.id)])

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            house_service.AddMembers(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == "House not found!"

    def test_it_adds_members_to_house_user_not_found(self, house_service: HouseStub, mf: ModelFactory):
        house = mf.house.house()
        user_id = uuid.uuid4()
        request = AddMembersPayload(house_id=str(house.id), user_ids=[str(user_id)])

        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            house_service.AddMembers(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.NOT_FOUND
        assert exception.details() == "User not found!"

    def test_it_adds_members_to_house_user_already_exists(self, house_service: HouseStub, mf: ModelFactory):
        house = mf.house.house()
        user = mf.user.user()
        request = AddMembersPayload(house_id=str(house.id), user_ids=[str(user.id)])

        house_service.AddMembers(request)
        with pytest.raises(grpc._channel._InactiveRpcError) as e:
            house_service.AddMembers(request)

        exception = e.value.exception()
        assert exception.code() == grpc.StatusCode.ALREADY_EXISTS
        assert exception.details() == f"User {user.id} already exists in the house {house.id}!"

    def test_it_removes_member(self, house_service: HouseStub, mf: ModelFactory):
        house = mf.house.house()
        user = mf.user.user()
        request = RemoveMemberPayload(house_id=str(house.id), user_id=str(user.id))

        response = house_service.RemoveMember(request)
        assert response.house_id == str(house.id)
        assert response.user_id == str(user.id)

    def test_it_gets_members(self, house_service: HouseStub, mf: ModelFactory):
        house = mf.house.house()
        user = mf.user.user()
        mf.house.house_member(house_id=house.id, user_id=user.id)

        request = GetPayload(house_id=str(house.id))
        response = house_service.GetMembers(request)

        assert response.house_id == str(house.id)
        assert len(response.users) == 1
        assert response.users[0].id == str(user.id)
        assert response.users[0].first_name == user.first_name
        assert response.users[0].last_name == user.last_name
        assert response.users[0].email == user.email
