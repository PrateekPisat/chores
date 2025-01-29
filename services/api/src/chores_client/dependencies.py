from collections.abc import Generator
from typing import Annotated

import grpc
from chores.grpc_generated.chores_pb2_grpc import HouseStub, TaskStub, UsersStub
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from chores_client.config import Config, load_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def config() -> Config:
    return load_config()


ConfigDep = Annotated[Config, Depends(config)]


def get_channel_credentials(
    config: ConfigDep, sub_path: str, hostname: str
) -> grpc.ChannelCredentials:
    base_path = f"{config.cert.certs_path}/{sub_path}"

    return grpc.ssl_channel_credentials(
        open(f"{base_path}/rootCA.crt", "rb").read(),
        open(f"{base_path}/{hostname}.key", "rb").read(),
        open(f"{base_path}/{hostname}.crt", "rb").read(),
    )


def house_client(config: ConfigDep) -> Generator[HouseStub, None, None]:
    with grpc.secure_channel(
        config.house_service.url,
        get_channel_credentials(config, config.house_service.cert_path, config.house_service.host),
    ) as channel:
        yield HouseStub(channel)


def users_client(config: ConfigDep) -> Generator[UsersStub, None, None]:
    with grpc.secure_channel(
        config.user_service.url,
        get_channel_credentials(config, config.user_service.cert_path, config.user_service.host),
    ) as channel:
        yield UsersStub(channel)


def task_client(config: ConfigDep) -> Generator[TaskStub, None, None]:
    with grpc.secure_channel(
        config.task_service.url,
        get_channel_credentials(config, config.task_service.cert_path, config.task_service.host),
    ) as channel:
        yield TaskStub(channel)


HouseClientDep = Annotated[Generator[HouseStub, None, None], Depends(house_client)]
UsersClientDep = Annotated[Generator[UsersStub, None, None], Depends(users_client)]
TaskClientDep = Annotated[Generator[TaskStub, None, None], Depends(task_client)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
