from chores.grpc_generated.chores_pb2 import LoginPayload, RegisterPayload
from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, field_validator, ValidationInfo


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        populate_by_name=True, from_attributes=True, arbitrary_types_allowed=True
    )


class AuthToken(BaseModel):
    token: str = Field(..., description="The token for the user", min_length=1)


class LoginRequest(BaseModel):
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

    @property
    def to_grpc_model(self):
        return LoginPayload(email=self.email, password=self.password)


class LoginResponse(BaseModel):
    user_id: str = Field(..., description="The ID of the user that was created", min_length=1)
    token: str = Field(..., description="The token for the user", min_length=1)


class RegisterRequest(LoginRequest):
    confirm_password: str = Field(
        ..., description="The password confirmation", min_length=1, alias="confirmPassword"
    )
    first_name: str = Field(
        ..., description="The first name of the user", min_length=1, alias="firstName"
    )
    last_name: str = Field(
        ..., description="The last name of the user", min_length=1, alias="lastName"
    )

    @field_validator("confirm_password", mode="before")
    @classmethod
    def validate_passwords(cls, value: str, info: ValidationInfo):
        password = info.data.get("password")
        if not password:
            return value

        if value != password:
            raise ValueError("Passwords do not match")
        return value

    @property
    def to_grpc_model(self):
        return RegisterPayload(
            email=self.email,
            password=self.password,
            confirm_password=self.confirm_password,
            first_name=self.first_name,
            last_name=self.last_name,
        )


class RegisterResponse(LoginResponse): ...


class UserId(BaseModel):
    user_id: str = Field(..., description="The ID of the user", min_length=1)


class User(UserId):
    email: str = Field(..., description="The email of the user", min_length=1)
    first_name: str = Field(..., description="The first name of the user", min_length=1)
    last_name: str = Field(..., description="The last name of the user", min_length=1)


class UpdateUserRequest(BaseModel):
    email: str = Field(..., description="The email of the user", min_length=1)
    first_name: str = Field(
        ..., description="The first name of the user", min_length=1, alias="firstName"
    )
    last_name: str = Field(
        ..., description="The last name of the user", min_length=1, alias="lastName"
    )


class SearchUserRequest(BaseModel):
    email: str = Field(..., description="The email of the user", min_length=1)
