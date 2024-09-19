from dependency_injector import containers, providers

from chores.config import Config
from chores.db import get_session


class Container(containers.DeclarativeContainer):
    config = providers.Factory(Config)
    postgres = providers.Factory(get_session, config=config)
