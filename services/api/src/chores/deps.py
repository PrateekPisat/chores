from dependency_injector import containers, providers

from chores.config import load_config
from chores.db import get_session


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".users_server"])

    config = providers.Callable(load_config)
    postgres = providers.Callable(get_session, config=config)
