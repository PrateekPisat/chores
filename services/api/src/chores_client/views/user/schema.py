from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        populate_by_name=True, from_attributes=True, arbitrary_types_allowed=True
    )


class AuthToken(BaseModel):
    token: str = Field(..., description="The token for the user", min_length=1)


class UserId(BaseModel):
    user_id: str = Field(..., description="The ID of the user", min_length=1)


class User(UserId):
    email: str = Field(..., description="The email of the user", min_length=1)
    first_name: str = Field(..., description="The first name of the user", min_length=1)
    last_name: str = Field(..., description="The last name of the user", min_length=1)
    sub: str = Field(..., description="The Auth0 sub", min_length=1)
    picture: str | None = Field(None, description="The picture of the user")
    nickname: str | None = Field(None, description="The nickname of the user", alias="nickname")


class UpdateUserRequest(BaseModel):
    email: str = Field(..., description="The email of the user", min_length=1)
    first_name: str = Field(
        ..., description="The first name of the user", min_length=1, alias="firstName"
    )
    last_name: str = Field(
        ..., description="The last name of the user", min_length=1, alias="lastName"
    )
    picture: str | None = Field(None, description="The picture of the user")
    nickname: str | None = Field(None, description="The nickname of the user")
    sub: str = Field(..., description="The Auth0 sub", min_length=1)


class SearchUserRequest(BaseModel):
    email: str = Field(..., description="The email of the user", min_length=1)


class SyncUserRequest(UpdateUserRequest): ...
