from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

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

class CreatePayload(_message.Message):
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
