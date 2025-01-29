from __future__ import annotations

from typing import Annotated

from dataclass_settings import Env, load_settings
from pydantic import BaseModel


class Config(BaseModel):
    logging: LoggingConfig
    house_service: HouseServiceConfig
    user_service: UserServiceConfig
    task_service: TaskServiceConfig
    cert: CertConfig

    environment: Annotated[str | None, Env("ENVIRONMENT")] = None


class LoggingConfig(BaseModel):
    level: Annotated[str, Env("LOGGING_LEVEL")] = "INFO"


class ChoresServiceConfig(BaseModel):
    service_base_url: Annotated[str, Env("SERVICE_BASE_URL")] = "localhost"


class UserServiceConfig(ChoresServiceConfig):
    port: Annotated[int, Env("USERS_SERVICE_PORT")] = 50051
    host: Annotated[str, Env("USERS_SERVICE_HOST")] = "localhost"
    cert_path: Annotated[str | None, Env("USERS_SERVICE_CERT_PATH")] = "users_service"

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class TaskServiceConfig(ChoresServiceConfig):
    port: Annotated[int, Env("TASK_SERVICE_PORT")] = 50053
    host: Annotated[str, Env("TASK_SERVICE_HOST")] = "localhost"
    cert_path: Annotated[str | None, Env("TASK_SERVICE_CERT_PATH")] = "task_service"

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class HouseServiceConfig(ChoresServiceConfig):
    port: Annotated[int, Env("HOUSE_SERVICE_PORT")] = 50052
    host: Annotated[str, Env("HOUSE_SERVICE_HOST")] = "localhost"
    cert_path: Annotated[str | None, Env("HOUSE_SERVICE_CERT_PATH")] = "house_service"

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class CertConfig(BaseModel):
    certs_path: Annotated[str | None, Env("CERTS_PATH")] = None


def load_config():
    return load_settings(Config)
