import logging
from logging.config import fileConfig
from typing import Annotated, cast

from alembic import context
from chores.models.base import metadata
from dataclass_settings import Env, load_settings
from pydantic import BaseModel
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy_declarative_extensions import register_alembic_events

logger = logging.getLogger("alembic.env")
logging.getLogger("alembic.ddl.postgresql").setLevel("WARNING")
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
register_alembic_events(roles=True, schemas=True, grants=True, rows=True)


class PostgresConfig(BaseModel):
    host: Annotated[str, Env("DATABASE_HOST")]
    username: Annotated[str, Env("DATABASE_USERNAME")]
    password: Annotated[str, Env("DATABASE_PASSWORD")]
    database: Annotated[str, Env("DATABASE_DATABASE")]

    port: Annotated[int, Env("DATABASE_PORT")] = 5432
    drivername: str = "postgresql+psycopg2"


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = cast(Engine, context.config.attributes.get("connection", None))

    config = load_settings(PostgresConfig)
    context.config.set_main_option(
        "sqlalchemy.url", URL.create(**config.model_dump()).render_as_string(hide_password=False)
    )
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    def process_revision_directives(context, revision, directives):
        if context.config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=metadata,
            process_revision_directives=process_revision_directives,
            include_schemas=True,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
