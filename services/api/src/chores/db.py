import functools

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from chores.config import load_config


@functools.cache
def get_db() -> callable:
    config = load_config()

    url = sqlalchemy.engine.url.URL.create(**config.postgres.model_dump())
    engine = sqlalchemy.create_engine(url)

    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)  # noqa: N806

    def make_session():
        return Session()

    return make_session


def inject_db(fn=None, *, commit_on_success=False):
    def _inject_db(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            db = get_db()()

            try:
                result = fn(*args, **kwargs, db=db)
            except Exception:
                db.rollback()
                db.close()
                raise
            else:
                if commit_on_success:
                    db.commit()
            finally:
                db.close()

            return result

        return wrapper

    if fn is not None:
        return _inject_db(fn)
    return _inject_db
