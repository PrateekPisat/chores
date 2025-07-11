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

from chores_client.dependencies import UsersClientDep
from chores_client.views.user.schema import (
    SearchUserRequest,
    SyncUserRequest,
    UpdateUserRequest,
    User,
    UserId,
)


def get_user(user_id: str, users_client: UsersClientDep) -> User:
    user: GetUserResponse = users_client.GetUser(GetUserPayload(user_id=user_id))

    return User(
        userId=user.user_id,
        email=user.email,
        firstName=user.first_name,
        lastName=user.last_name,
        sub=user.sub,
        picture=user.picture,
        nickname=user.nickname,
    )


def check_update_payload(payload: UpdateUserRequest) -> UpdateUserRequest:
    return UpdateUserRequest(**payload.model_dump(by_alias=True))


def update_user(user_id: str, payload: UpdateUserRequest, users_client: UsersClientDep) -> UserId:
    user: UpdateUserResponse = users_client.UpdateUser(
        UpdateUserPayload(
            user_id=user_id,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
        )
    )
    return UserId(userId=user.user_id)


def delete_user(user_id: str, users_client: UsersClientDep) -> UserId:
    user: DeleteUserResponse = users_client.DeleteUser(DeleteUserPayload(user_id=user_id))
    return UserId(userId=user.user_id)


def search_user(payload: SearchUserRequest, users_client: UsersClientDep) -> list[User]:
    response: SearchUserResponse = users_client.SearchUser(
        SearchUserPayload(email=payload.email, chore_id=payload.chore_id)
    )
    return [
        User(
            user_id=user.user_id,
            email=user.email,
            firstName=user.first_name,
            lastName=user.last_name,
            sub=user.sub,
            picture=user.picture,
            nickname=user.nickname,
        )
        for user in response.users
    ]


def sync_user(payload: SyncUserRequest, users_client: UsersClientDep) -> User:
    response: SyncUserResponse = users_client.SyncUser(SyncUserPayload(**payload.model_dump()))
    return User(
        user_id=response.user.id,
        email=response.user.email,
        firstName=response.user.first_name,
        lastName=response.user.last_name,
        sub=response.user.sub,
        picture=response.user.picture,
        nickname=response.user.nickname,
    )
