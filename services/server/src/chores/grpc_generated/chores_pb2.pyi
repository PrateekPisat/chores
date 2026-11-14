from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import (
    ClassVar as _ClassVar,
)

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class Cadence(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DAILY: _ClassVar[Cadence]
    WEEKLY: _ClassVar[Cadence]
    MONTHLY: _ClassVar[Cadence]
    YEARLY: _ClassVar[Cadence]

DAILY: Cadence
WEEKLY: Cadence
MONTHLY: Cadence
YEARLY: Cadence

class User(_message.Message):
    __slots__ = ("id", "email", "first_name", "last_name", "sub", "picture", "nickname")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    SUB_FIELD_NUMBER: _ClassVar[int]
    PICTURE_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    first_name: str
    last_name: str
    sub: str
    picture: str
    nickname: str
    def __init__(
        self,
        id: str | None = ...,
        email: str | None = ...,
        first_name: str | None = ...,
        last_name: str | None = ...,
        sub: str | None = ...,
        picture: str | None = ...,
        nickname: str | None = ...,
    ) -> None: ...

class Chore(_message.Message):
    __slots__ = ("id", "name", "description", "cadence", "start_date", "end_date", "house_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    cadence: Cadence
    start_date: str
    end_date: str
    house_id: str
    def __init__(
        self,
        id: str | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        cadence: Cadence | str | None = ...,
        start_date: str | None = ...,
        end_date: str | None = ...,
        house_id: str | None = ...,
    ) -> None: ...

class CreateChorePayload(_message.Message):
    __slots__ = ("name", "description", "cadence", "start_date", "end_date", "house_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    cadence: Cadence
    start_date: str
    end_date: str
    house_id: str
    def __init__(
        self,
        name: str | None = ...,
        description: str | None = ...,
        cadence: Cadence | str | None = ...,
        start_date: str | None = ...,
        end_date: str | None = ...,
        house_id: str | None = ...,
    ) -> None: ...

class CreateChoreResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class GetChorePayload(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class GetChoreResponse(_message.Message):
    __slots__ = ("id", "name", "description", "cadence", "start_date", "end_date", "house_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    cadence: Cadence
    start_date: str
    end_date: str
    house_id: str
    def __init__(
        self,
        id: str | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        cadence: Cadence | str | None = ...,
        start_date: str | None = ...,
        end_date: str | None = ...,
        house_id: str | None = ...,
    ) -> None: ...

class ListChorePayload(_message.Message):
    __slots__ = ("house_id", "user_id")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    user_id: str
    def __init__(self, house_id: str | None = ..., user_id: str | None = ...) -> None: ...

class ListChoreResponse(_message.Message):
    __slots__ = ("chores",)
    CHORES_FIELD_NUMBER: _ClassVar[int]
    chores: _containers.RepeatedCompositeFieldContainer[GetChoreResponse]
    def __init__(self, chores: _Iterable[GetChoreResponse | _Mapping] | None = ...) -> None: ...

class UpdateChorePayload(_message.Message):
    __slots__ = ("id", "name", "description", "cadence", "start_date", "end_date", "house_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    cadence: Cadence
    start_date: str
    end_date: str
    house_id: str
    def __init__(
        self,
        id: str | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        cadence: Cadence | str | None = ...,
        start_date: str | None = ...,
        end_date: str | None = ...,
        house_id: str | None = ...,
    ) -> None: ...

class UpdateChoreResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class DeleteChorePayload(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class DeleteChoreResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class CreateDistributionPayload(_message.Message):
    __slots__ = ("chore_id", "user_ids")
    CHORE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    chore_id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, chore_id: str | None = ..., user_ids: _Iterable[str] | None = ...) -> None: ...

class CreateDistributionResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class GetDistributionPayload(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class GetDistributionResponse(_message.Message):
    __slots__ = ("chore", "users")
    CHORE_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    chore: Chore
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(
        self, chore: Chore | _Mapping | None = ..., users: _Iterable[User | _Mapping] | None = ...
    ) -> None: ...

class UpdateDistributionPayload(_message.Message):
    __slots__ = ("chore_id", "user_ids")
    CHORE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    chore_id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, chore_id: str | None = ..., user_ids: _Iterable[str] | None = ...) -> None: ...

class UpdateDistributionResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class DeleteDistributionPayload(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class DeleteDistributionResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class GetTaskPayload(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class GetTaskResponse(_message.Message):
    __slots__ = ("id", "chore", "user", "due_date", "completed_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHORE_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    chore: Chore
    user: User
    due_date: str
    completed_at: str
    def __init__(
        self,
        id: str | None = ...,
        chore: Chore | _Mapping | None = ...,
        user: User | _Mapping | None = ...,
        due_date: str | None = ...,
        completed_at: str | None = ...,
    ) -> None: ...

class ListTaskPayload(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: str | None = ...) -> None: ...

class ListTaskResponse(_message.Message):
    __slots__ = ("tasks",)
    TASKS_FIELD_NUMBER: _ClassVar[int]
    tasks: _containers.RepeatedCompositeFieldContainer[GetTaskResponse]
    def __init__(self, tasks: _Iterable[GetTaskResponse | _Mapping] | None = ...) -> None: ...

class UpdateTaskPayload(_message.Message):
    __slots__ = ("id", "due_date", "completed_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    due_date: str
    completed_at: str
    def __init__(self, id: str | None = ..., due_date: str | None = ..., completed_at: str | None = ...) -> None: ...

class UpdateTaskResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class DeleteTaskPayload(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class DeleteTaskResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: str | None = ...) -> None: ...

class CreatePayload(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: str | None = ...) -> None: ...

class CreateResponse(_message.Message):
    __slots__ = ("house_id",)
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    def __init__(self, house_id: str | None = ...) -> None: ...

class GetPayload(_message.Message):
    __slots__ = ("house_id",)
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    def __init__(self, house_id: str | None = ...) -> None: ...

class ListHousePayload(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: str | None = ...) -> None: ...

class SearchHousePayload(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: str | None = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ("house_id", "name")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    name: str
    def __init__(self, house_id: str | None = ..., name: str | None = ...) -> None: ...

class HouseResponse(_message.Message):
    __slots__ = ("house_id", "name")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    name: str
    def __init__(self, house_id: str | None = ..., name: str | None = ...) -> None: ...

class ListHousesResponse(_message.Message):
    __slots__ = ("houses",)
    HOUSES_FIELD_NUMBER: _ClassVar[int]
    houses: _containers.RepeatedCompositeFieldContainer[HouseResponse]
    def __init__(self, houses: _Iterable[HouseResponse | _Mapping] | None = ...) -> None: ...

class UpdatePayload(_message.Message):
    __slots__ = ("house_id", "name")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    name: str
    def __init__(self, house_id: str | None = ..., name: str | None = ...) -> None: ...

class UpdateResponse(_message.Message):
    __slots__ = ("house_id",)
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    def __init__(self, house_id: str | None = ...) -> None: ...

class DeletePayload(_message.Message):
    __slots__ = ("house_id",)
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    def __init__(self, house_id: str | None = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ("house_id",)
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    def __init__(self, house_id: str | None = ...) -> None: ...

class AddMembersPayload(_message.Message):
    __slots__ = ("house_id", "user_ids")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, house_id: str | None = ..., user_ids: _Iterable[str] | None = ...) -> None: ...

class AddMemberResponse(_message.Message):
    __slots__ = ("house_id", "user_ids")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, house_id: str | None = ..., user_ids: _Iterable[str] | None = ...) -> None: ...

class RemoveMemberPayload(_message.Message):
    __slots__ = ("house_id", "user_id")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    user_id: str
    def __init__(self, house_id: str | None = ..., user_id: str | None = ...) -> None: ...

class RemoveMemberResponse(_message.Message):
    __slots__ = ("house_id", "user_id")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    user_id: str
    def __init__(self, house_id: str | None = ..., user_id: str | None = ...) -> None: ...

class GetMembersResponse(_message.Message):
    __slots__ = ("house_id", "users")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, house_id: str | None = ..., users: _Iterable[User | _Mapping] | None = ...) -> None: ...

class GetUserPayload(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: str | None = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("user_id", "email", "first_name", "last_name", "sub", "picture", "nickname")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    SUB_FIELD_NUMBER: _ClassVar[int]
    PICTURE_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    email: str
    first_name: str
    last_name: str
    sub: str
    picture: str
    nickname: str
    def __init__(
        self,
        user_id: str | None = ...,
        email: str | None = ...,
        first_name: str | None = ...,
        last_name: str | None = ...,
        sub: str | None = ...,
        picture: str | None = ...,
        nickname: str | None = ...,
    ) -> None: ...

class UpdateUserPayload(_message.Message):
    __slots__ = ("user_id", "email", "first_name", "last_name")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    email: str
    first_name: str
    last_name: str
    def __init__(
        self,
        user_id: str | None = ...,
        email: str | None = ...,
        first_name: str | None = ...,
        last_name: str | None = ...,
    ) -> None: ...

class UpdateUserResponse(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: str | None = ...) -> None: ...

class DeleteUserPayload(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: str | None = ...) -> None: ...

class DeleteUserResponse(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: str | None = ...) -> None: ...

class SearchUserPayload(_message.Message):
    __slots__ = ("email", "chore_id")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    CHORE_ID_FIELD_NUMBER: _ClassVar[int]
    email: str
    chore_id: str
    def __init__(self, email: str | None = ..., chore_id: str | None = ...) -> None: ...

class SearchUserResponse(_message.Message):
    __slots__ = ("users",)
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[GetUserResponse]
    def __init__(self, users: _Iterable[GetUserResponse | _Mapping] | None = ...) -> None: ...

class SyncUserPayload(_message.Message):
    __slots__ = ("email", "first_name", "last_name", "sub", "picture", "nickname")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    SUB_FIELD_NUMBER: _ClassVar[int]
    PICTURE_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    first_name: str
    last_name: str
    sub: str
    picture: str
    nickname: str
    def __init__(
        self,
        email: str | None = ...,
        first_name: str | None = ...,
        last_name: str | None = ...,
        sub: str | None = ...,
        picture: str | None = ...,
        nickname: str | None = ...,
    ) -> None: ...

class SyncUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: User | _Mapping | None = ...) -> None: ...
