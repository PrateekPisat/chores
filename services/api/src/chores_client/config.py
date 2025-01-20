from __future__ import annotations

from typing import Annotated

from dataclass_settings import Env, load_settings
from pydantic import BaseModel


class Config(BaseModel):
    logging: LoggingConfig
    chores_service: ChoresServiceConfig
    certs_path: Annotated[str | None, Env("CERTS_PATH")] = None

    environment: Annotated[str | None, Env("ENVIRONMENT")] = None


class LoggingConfig(BaseModel):
    level: Annotated[str, Env("LOGGING_LEVEL")] = "INFO"


class ChoresServiceConfig(BaseModel):
    service_base_url: Annotated[str, Env("SERVICE_BASE_URL")] = "localhost"
    user_service_port: Annotated[int, Env("USER_SERVICE_PORT")] = 50051
    house_service_port: Annotated[int, Env("HOUSE_SERVICE_PORT")] = 50052
    task_service_port: Annotated[int, Env("TASK_SERVICE_PORT")] = 50053

    @property
    def user_service_url(self) -> str:
        return f"{self.service_base_url}:{self.user_service_port}"

    @property
    def house_service_url(self) -> str:
        return f"{self.service_base_url}:{self.house_service_port}"

    @property
    def task_service_url(self) -> str:
        return f"{self.service_base_url}:{self.task_service_port}"


def load_config():
    return load_settings(Config)
