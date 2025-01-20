from chores.grpc_generated.chores_pb2 import (
    DeleteUserPayload,
    DeleteUserResponse,
    GetUserPayload,
    GetUserResponse,
    LogoutPayload,
    LogoutResponse,
    SearchUserPayload,
    SearchUserResponse,
    UpdateUserPayload,
    UpdateUserResponse,
)

from chores_client.dependencies import TokenDep, UsersClientDep
from chores_client.views.user.schema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    SearchUserRequest,
    UpdateUserRequest,
    User,
    UserId,
)


def register_user(payload: RegisterRequest, users_client: UsersClientDep) -> RegisterResponse:
    user = users_client.Register(payload.to_grpc_model)
    return RegisterResponse(user_id=user.user_id, token=user.token)


def check_user_payload(payload: RegisterRequest) -> RegisterRequest:
    return RegisterRequest(**payload.model_dump())


def login_user(payload: LoginRequest, users_client: UsersClientDep) -> LoginResponse:
    user = users_client.Login(payload.to_grpc_model)
    return LoginResponse(user_id=user.user_id, token=user.token)


def check_login_payload(payload: LoginRequest) -> LoginRequest:
    return LoginRequest(**payload.model_dump())


def logout_user(payload: UserId, users_client: UsersClientDep, token: TokenDep) -> UserId:
    response: LogoutResponse = users_client.Logout(
        LogoutPayload(user_id=payload.user_id, token=token),
        metadata=[("authorization", f"Bearer {token}")],
    )

    return UserId(user_id=response.user_id)


def get_user(user_id: str, users_client: UsersClientDep, token: TokenDep) -> User:
    user: GetUserResponse = users_client.GetUser(
        GetUserPayload(user_id=user_id), metadata=[("authorization", f"Bearer {token}")]
    )

    return User(
        user_id=user.user_id, email=user.email, first_name=user.first_name, last_name=user.last_name
    )


def check_update_payload(payload: UpdateUserRequest) -> UpdateUserRequest:
    return UpdateUserRequest(**payload.model_dump())


def update_user(
    user_id: str, payload: UpdateUserRequest, users_client: UsersClientDep, token: TokenDep
) -> UserId:
    user: UpdateUserResponse = users_client.UpdateUser(
        UpdateUserPayload(user_id=user_id, **payload.model_dump()),
        metadata=[("authorization", f"Bearer {token}")],
    )
    return UserId(user_id=user.user_id)


def delete_user(user_id: str, users_client: UsersClientDep, token: TokenDep) -> UserId:
    user: DeleteUserResponse = users_client.DeleteUser(
        DeleteUserPayload(user_id=user_id), metadata=[("authorization", f"Bearer {token}")]
    )
    return UserId(user_id=user.user_id)


def search_user(
    payload: SearchUserRequest, users_client: UsersClientDep, token: TokenDep
) -> list[User]:
    response: SearchUserResponse = users_client.SearchUser(
        SearchUserPayload(email=payload.email), metadata=[("authorization", f"Bearer {token}")]
    )
    return [
        User(
            user_id=user.user_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        for user in response.users
    ]
