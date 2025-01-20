from typing import Literal

import pendulum
from chores.grpc_generated.chores_pb2 import Cadence, CreateChorePayload
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, field_validator

from chores_client.views.user.schema import User

ENUM_MAP = {
    "DAILY": Cadence.DAILY,
    "WEEKLY": Cadence.WEEKLY,
    "MONTHLY": Cadence.MONTHLY,
    "YEARLY": Cadence.YEARLY,
}


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        populate_by_name=True, from_attributes=True, arbitrary_types_allowed=True
    )


class ChoreId(BaseModel):
    id: str = Field(..., min_length=1)


class ChoreDetails(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    cadence: Literal["DAILY", "WEEKLY", "MONTHLY", "YEARLY"]
    start_date: str = Field(..., min_length=1, alias="startDate")
    end_date: str = Field(..., min_length=1, alias="endDate")

    @field_validator("start_date", "end_date", mode="after", check_fields=True)
    @classmethod
    def parse_date(cls, value: str) -> str:
        try:
            return pendulum.from_format(value, "YYYY-MM-DD").date().isoformat()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

    def grpc_model_dump(self):
        return CreateChorePayload(
            name=self.name,
            description=self.description,
            cadence=ENUM_MAP[self.cadence],
            start_date=self.start_date,
            end_date=self.end_date,
        )


class Chore(ChoreId, ChoreDetails): ...


class UserIds(BaseModel):
    user_ids: list[str] = Field(..., min_length=1, default_factory=list, alias="userIds")


class ChoreDistribution(BaseModel):
    chore: Chore
    users: list[User] = Field(..., default_factory=list)


class TaskId(BaseModel):
    id: str = Field(..., min_length=1)


class Task(TaskId):
    chore: Chore
    user: User
    due_date: str | None = Field(None, alias="dueDate")
    completed_at: str | None = Field(None, alias="completedAt")


class UpdateTask(BaseModel):
    due_date: str | None = Field(None, alias="dueDate")
    completed_at: str | None = Field(None, alias="completedAt")
