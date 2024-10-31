from __future__ import annotations

from typing import Annotated

from dataclass_settings import Env, load_settings
from pydantic import BaseModel


class Config(BaseModel):
    logging: LoggingConfig
    postgres: PostgresConfig
    cryptography: CryptographyConfig

    environment: Annotated[str | None, Env("ENVIRONMENT")] = None


class LoggingConfig(BaseModel):
    level: Annotated[str, Env("LOGGING_LEVEL")] = "INFO"


class PostgresConfig(BaseModel):
    host: Annotated[str, Env("DATABASE_HOST")]
    username: Annotated[str, Env("DATABASE_USERNAME")]
    password: Annotated[str, Env("DATABASE_PASSWORD")]
    database: Annotated[str, Env("DATABASE_DATABASE")]

    port: Annotated[int, Env("DATABASE_PORT")] = 5432
    drivername: str = "postgresql+psycopg2"


class CryptographyConfig(BaseModel):
    secret_key: Annotated[str, Env("SECRET_KEY")]


def load_config():
    return load_settings(Config)
