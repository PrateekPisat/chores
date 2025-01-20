import pendulum
from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, field_validator, ValidationInfo


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True, arbitrary_types_allowed=True)


class CreateHousePayload(BaseModel):
    name: str = Field(..., description="The name of the house", min_length=1)


class UpdateHousePayload(CreateHousePayload):
    house_id: str = Field(..., description="The ID of the house to update", min_length=1)


class LoginUserPayload(BaseModel):
    email: str = Field(..., description="The email of the user", min_length=1)
    password: str = Field(..., description="The password of the user", min_length=1)

    @field_validator("email", mode="after", check_fields=True)
    @classmethod
    def validate_email(cls, value: str) -> str:
        try:
            email = validate_email(value, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValueError(str(e))

        return email.normalized


class RegisterUserPayload(LoginUserPayload):
    confirm_password: str = Field(..., description="The password confirmation", min_length=1)
    first_name: str = Field(..., description="The first name of the user", min_length=1)
    last_name: str = Field(..., description="The last name of the user", min_length=1)

    @field_validator("confirm_password", mode="before")
    @classmethod
    def validate_passwords(cls, value: str, info: ValidationInfo):
        password = info.data.get("password")
        if not password:
            return value

        if value != password:
            raise ValueError("Passwords do not match")
        return value


class UpdateUserPayload(LoginUserPayload):
    user_id: str = Field(..., description="The ID of the user to update", min_length=1)
    first_name: str = Field(..., description="The first name of the user", min_length=1)
    last_name: str = Field(..., description="The last name of the user", min_length=1)


class CreateChorePayload(BaseModel):
    name: str = Field(..., description="The name of the chore.", min_length=1)
    description: str = Field(..., description="The description of the chore.", min_length=1)
    cadence: str = Field(..., description="The cadence of the chore", min_length=1)
    start_date: str = Field(..., description="The start date of the chore", min_length=1)
    end_date: str = Field(..., description="The end date of the chore.", min_length=1)

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def parse_date(cls, value: str | None) -> str | None:
        if not value:
            return None

        try:
            return pendulum.parse(value).date().isoformat()  # type: ignore
        except ValueError:
            raise ValueError("Invalid date format")


class UpdateChorePayload(CreateChorePayload):
    chore_id: str = Field(..., description="The ID of the chore to update", min_length=1)


class CreateDistributionPayload(BaseModel):
    chore_id: str = Field(..., description="The ID of the chore.", min_length=1)
    user_ids: list[str] = Field(
        description="A list of user ids to include in the chore", default_factory=list, min_length=1
    )


class UpdateDistributionPayload(CreateDistributionPayload): ...
