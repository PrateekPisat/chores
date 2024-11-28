from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

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
    __slots__ = ("id", "email", "first_name", "last_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    first_name: str
    last_name: str
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ...) -> None: ...

class Chore(_message.Message):
    __slots__ = ("id", "name", "description", "cadence", "start_date", "end_date")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    cadence: Cadence
    start_date: str
    end_date: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., cadence: _Optional[_Union[Cadence, str]] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ...) -> None: ...

class CreateChorePayload(_message.Message):
    __slots__ = ("name", "description", "cadence", "start_date", "end_date")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    cadence: Cadence
    start_date: str
    end_date: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., cadence: _Optional[_Union[Cadence, str]] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ...) -> None: ...

class CreateChoreErrorsResponse(_message.Message):
    __slots__ = ("name", "description", "cadence", "start_date", "end_date")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    cadence: str
    start_date: str
    end_date: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., cadence: _Optional[str] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ...) -> None: ...

class CreateChoreResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetChorePayload(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetChoreResponse(_message.Message):
    __slots__ = ("id", "name", "description", "cadence", "start_date", "end_date")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    cadence: Cadence
    start_date: str
    end_date: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., cadence: _Optional[_Union[Cadence, str]] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ...) -> None: ...

class UpdateChorePayload(_message.Message):
    __slots__ = ("id", "name", "description", "cadence", "start_date", "end_date")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    cadence: Cadence
    start_date: str
    end_date: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., cadence: _Optional[_Union[Cadence, str]] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ...) -> None: ...

class UpdateChoreErrorsResponse(_message.Message):
    __slots__ = ("id", "name", "description", "cadence", "start_date", "end_date")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CADENCE_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    cadence: str
    start_date: str
    end_date: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., cadence: _Optional[str] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ...) -> None: ...

class UpdateChoreResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteChorePayload(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteChoreResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CreateDistributionPayload(_message.Message):
    __slots__ = ("chore_id", "user_ids")
    CHORE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    chore_id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, chore_id: _Optional[str] = ..., user_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateDistributionErrorResponse(_message.Message):
    __slots__ = ("chore_id", "user_ids")
    CHORE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    chore_id: str
    user_ids: str
    def __init__(self, chore_id: _Optional[str] = ..., user_ids: _Optional[str] = ...) -> None: ...

class CreateDistributionResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDistributionPayload(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDistributionResponse(_message.Message):
    __slots__ = ("chore", "users")
    CHORE_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    chore: Chore
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, chore: _Optional[_Union[Chore, _Mapping]] = ..., users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...

class UpdateDistributionPayload(_message.Message):
    __slots__ = ("chore_id", "user_ids")
    CHORE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    chore_id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, chore_id: _Optional[str] = ..., user_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateDistributionErrorResponse(_message.Message):
    __slots__ = ("chore_id", "user_ids")
    CHORE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    chore_id: str
    user_ids: str
    def __init__(self, chore_id: _Optional[str] = ..., user_ids: _Optional[str] = ...) -> None: ...

class UpdateDistributionResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteDistributionPayload(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteDistributionResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetTaskPayload(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

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
    def __init__(self, id: _Optional[str] = ..., chore: _Optional[_Union[Chore, _Mapping]] = ..., user: _Optional[_Union[User, _Mapping]] = ..., due_date: _Optional[str] = ..., completed_at: _Optional[str] = ...) -> None: ...

class UpdateTaskPayload(_message.Message):
    __slots__ = ("id", "due_date", "completed_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    due_date: str
    completed_at: str
    def __init__(self, id: _Optional[str] = ..., due_date: _Optional[str] = ..., completed_at: _Optional[str] = ...) -> None: ...

class UpdateTaskResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteTaskPayload(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteTaskResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CreatePayload(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CreateErrorResponse(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class CreateResponse(_message.Message):
    __slots__ = ("house_id",)
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    def __init__(self, house_id: _Optional[str] = ...) -> None: ...

class GetPayload(_message.Message):
    __slots__ = ("house_id",)
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    def __init__(self, house_id: _Optional[str] = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ("house_id", "name")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    name: str
    def __init__(self, house_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class UpdatePayload(_message.Message):
    __slots__ = ("house_id", "name")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    name: str
    def __init__(self, house_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class UpdateErrorResponse(_message.Message):
    __slots__ = ("house_id", "name")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    name: str
    def __init__(self, house_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class UpdateResponse(_message.Message):
    __slots__ = ("house_id",)
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    def __init__(self, house_id: _Optional[str] = ...) -> None: ...

class DeletePayload(_message.Message):
    __slots__ = ("house_id",)
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    def __init__(self, house_id: _Optional[str] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ("house_id",)
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    def __init__(self, house_id: _Optional[str] = ...) -> None: ...

class AddMembersPayload(_message.Message):
    __slots__ = ("house_id", "user_ids")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, house_id: _Optional[str] = ..., user_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AddMemberResponse(_message.Message):
    __slots__ = ("house_id", "user_ids")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_IDS_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    user_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, house_id: _Optional[str] = ..., user_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class RemoveMemberPayload(_message.Message):
    __slots__ = ("house_id", "user_id")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    user_id: str
    def __init__(self, house_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class RemoveMemberResponse(_message.Message):
    __slots__ = ("house_id", "user_id")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    user_id: str
    def __init__(self, house_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GetMembersResponse(_message.Message):
    __slots__ = ("house_id", "users")
    HOUSE_ID_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    house_id: str
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, house_id: _Optional[str] = ..., users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...

class RegisterPayload(_message.Message):
    __slots__ = ("email", "password", "confirm_password", "first_name", "last_name")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    confirm_password: str
    first_name: str
    last_name: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ..., confirm_password: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ...) -> None: ...

class RegisterErrorResponse(_message.Message):
    __slots__ = ("email", "password", "confirm_password", "first_name", "last_name")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    confirm_password: str
    first_name: str
    last_name: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ..., confirm_password: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ...) -> None: ...

class RegisterResponse(_message.Message):
    __slots__ = ("user_id", "token")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    token: str
    def __init__(self, user_id: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class LoginPayload(_message.Message):
    __slots__ = ("email", "password")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class LoginErrorResponse(_message.Message):
    __slots__ = ("email", "password")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ("user_id", "token")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    token: str
    def __init__(self, user_id: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class GetUserPayload(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("user_id", "email", "first_name", "last_name")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    email: str
    first_name: str
    last_name: str
    def __init__(self, user_id: _Optional[str] = ..., email: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ...) -> None: ...

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
    def __init__(self, user_id: _Optional[str] = ..., email: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ...) -> None: ...

class UpdateUserErrorResponse(_message.Message):
    __slots__ = ("user_id", "email", "first_name", "last_name")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    email: str
    first_name: str
    last_name: str
    def __init__(self, user_id: _Optional[str] = ..., email: _Optional[str] = ..., first_name: _Optional[str] = ..., last_name: _Optional[str] = ...) -> None: ...

class UpdateUserResponse(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class DeleteUserPayload(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class DeleteUserResponse(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class SearchUserPayload(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class SearchUserResponse(_message.Message):
    __slots__ = ("users",)
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[GetUserResponse]
    def __init__(self, users: _Optional[_Iterable[_Union[GetUserResponse, _Mapping]]] = ...) -> None: ...
