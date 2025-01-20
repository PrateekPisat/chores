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


def get_channel_credentials(config: ConfigDep):
    return grpc.ssl_channel_credentials(
        open(f"{config.certs_path}/rootCA.crt", "rb").read(),
        open(f"{config.certs_path}/localhost.key", "rb").read(),
        open(f"{config.certs_path}/localhost.crt", "rb").read(),
    )


ChannelCredentialsDep = Annotated[grpc.ChannelCredentials, Depends(get_channel_credentials)]


def house_client(
    config: ConfigDep, channel_credentials: ChannelCredentialsDep
) -> Generator[HouseStub, None, None]:
    with grpc.secure_channel(
        config.chores_service.house_service_url, channel_credentials
    ) as channel:
        yield HouseStub(channel)


def users_client(
    config: ConfigDep, channel_credentials: ChannelCredentialsDep
) -> Generator[UsersStub, None, None]:
    with grpc.secure_channel(
        config.chores_service.user_service_url, channel_credentials
    ) as channel:
        yield UsersStub(channel)


def task_client(
    config: ConfigDep, channel_credentials: ChannelCredentialsDep
) -> Generator[TaskStub, None, None]:
    with grpc.secure_channel(
        config.chores_service.task_service_url, channel_credentials
    ) as channel:
        yield TaskStub(channel)


HouseClientDep = Annotated[Generator[HouseStub, None, None], Depends(house_client)]
UsersClientDep = Annotated[Generator[UsersStub, None, None], Depends(users_client)]
TaskClientDep = Annotated[Generator[TaskStub, None, None], Depends(task_client)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
