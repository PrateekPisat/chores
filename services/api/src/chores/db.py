from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from chores.config import Config


def get_session(config: Config) -> callable:
    url = sqlalchemy.engine.url.URL.create(**config.postgres.model_dump())
    engine = sqlalchemy.create_engine(url)

    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)

    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@dataclass
class Database:
    config: Config

    @cached_property
    def config_dump(self):
        return self.config.postgres.model_dump()

    @contextmanager
    def session(self):
        url = sqlalchemy.engine.url.URL.create(**self.config_dump)
        engine = sqlalchemy.create_engine(url)

        session_factory = sessionmaker(bind=engine)
        session = scoped_session(session_factory)
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
