from chores.grpc_generated.chores_pb2 import (
    AddMemberResponse,
    AddMembersPayload,
    CreatePayload,
    DeletePayload,
    DeleteResponse,
    GetMembersResponse,
    GetPayload,
    ListHousePayload,
    ListHousesResponse,
    RemoveMemberPayload,
    RemoveMemberResponse,
    SearchHousePayload,
    UpdatePayload,
    UpdateResponse,
)

from chores_client.dependencies import HouseClientDep, TokenDep
from chores_client.views.house.schema import (
    House,
    HouseId,
    HouseMemberDetails,
    HouseMembers,
    HouseResponse,
)
from chores_client.views.user.schema import User


def create_house(payload: House, house_client: HouseClientDep, token: TokenDep) -> HouseId:
    house = house_client.Create(
        CreatePayload(name=payload.name), metadata=[("authorization", f"Bearer {token}")]
    )
    return HouseId(id=house.house_id)


def check_house_payload(payload: House) -> House:
    return House(**payload.model_dump())


def list_houses(user_id: str, house_client: HouseClientDep, token: TokenDep) -> list[HouseResponse]:
    response: ListHousesResponse = house_client.ListHouses(
        ListHousePayload(user_id=user_id), metadata=[("authorization", f"Bearer {token}")]
    )
    return [HouseResponse(name=house.name, id=house.house_id) for house in response.houses]


def search(payload: House, house_client: HouseClientDep, token: TokenDep) -> list[HouseResponse]:
    response: ListHousesResponse = house_client.SearchHouse(
        SearchHousePayload(name=payload.name), metadata=[("authorization", f"Bearer {token}")]
    )
    return [HouseResponse(name=house.name, id=house.house_id) for house in response.houses]


def get_house(house_id: str, house_client: HouseClientDep, token: TokenDep) -> House:
    house = house_client.Get(
        GetPayload(house_id=house_id), metadata=[("authorization", f"Bearer {token}")]
    )
    return House(name=house.name)


def check_update_payload(payload: House) -> House:
    return House(**payload.model_dump())


def update_house(
    house_id: str, payload: House, house_client: HouseClientDep, token: TokenDep
) -> HouseId:
    house: UpdateResponse = house_client.Update(
        UpdatePayload(house_id=house_id, name=payload.name),
        metadata=[("authorization", f"Bearer {token}")],
    )
    return HouseId(id=house.house_id)


def delete_house(house_id: str, house_client: HouseClientDep, token: TokenDep) -> HouseId:
    response: DeleteResponse = house_client.Delete(
        DeletePayload(house_id=house_id), metadata=[("authorization", f"Bearer {token}")]
    )
    return HouseId(id=response.house_id)


def add_member(
    payload: HouseMembers, house_client: HouseClientDep, token: TokenDep
) -> HouseMembers:
    response: AddMemberResponse = house_client.AddMembers(
        AddMembersPayload(house_id=payload.house_id, user_ids=payload.user_ids),
        metadata=[("authorization", f"Bearer {token}")],
    )
    return HouseMembers(houseId=response.house_id, user_ids=response.user_ids)


def remove_member(
    house_id: str, user_id: str, house_client: HouseClientDep, token: TokenDep
) -> HouseMembers:
    response: RemoveMemberResponse = house_client.RemoveMember(
        RemoveMemberPayload(house_id=house_id, user_id=user_id),
        metadata=[("authorization", f"Bearer {token}")],
    )
    return HouseMembers(houseId=response.house_id, user_ids=[response.user_id])


def get_members(house_id: str, house_client: HouseClientDep, token: TokenDep) -> HouseMemberDetails:
    response: GetMembersResponse = house_client.GetMembers(
        GetPayload(house_id=house_id), metadata=[("authorization", f"Bearer {token}")]
    )
    return HouseMemberDetails(
        houseId=response.house_id,
        users=[
            User(
                user_id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            for user in response.users
        ],
    )
