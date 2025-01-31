from argon2 import PasswordHasher
from dependency_injector import containers, providers

from chores.config import load_config
from chores.db import Database


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".users_server", ".house_server"])

    config = providers.Callable(load_config)
    database = providers.Singleton(Database, config=config)
    password_hasher = providers.Factory(PasswordHasher)
