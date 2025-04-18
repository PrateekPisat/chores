from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from chores_client.views.user.schema import User


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        populate_by_name=True, from_attributes=True, arbitrary_types_allowed=True
    )


class House(BaseModel):
    name: str = Field(..., min_length=1)


class HouseId(BaseModel):
    id: str = Field(..., min_length=1)


class HouseResponse(BaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)


class HouseMembers(BaseModel):
    house_id: str = Field(..., min_length=1, alias="houseId")
    user_ids: list[str] = Field(..., min_length=1, alias="userIds")


class HouseMemberDetails(BaseModel):
    house_id: str = Field(..., min_length=1, alias="houseId")
    users: list[User] = Field(..., default_factory=list)
