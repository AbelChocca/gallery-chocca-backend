from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool
from sqlalchemy.engine import URL, make_url
from sqlmodel import SQLModel

from app.core.alembic.alembic_settings import alembic_settings
from app.infra.db.model_registry import * # noqa: F401, F403

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = SQLModel.metadata

def get_alembic_db_url() -> URL:
    if alembic_settings.DATABASE_URL:
        url = make_url(alembic_settings.DATABASE_URL)

        if not url.drivername.startswith("postgresql"):
            raise ValueError("DATABASE_URL debe utilizar PostgreSQL")

        return url.set(drivername="postgresql+psycopg2")

    if not all((
        alembic_settings.POSTGRES_USER,
        alembic_settings.POSTGRES_PASSWORD,
        alembic_settings.POSTGRES_HOST,
        alembic_settings.POSTGRES_DB,
    )):
        raise ValueError("Configuración PostgreSQL incompleta")

    return URL.create(
        drivername="postgresql+psycopg2",
        username=alembic_settings.POSTGRES_USER,
        password=alembic_settings.POSTGRES_PASSWORD,
        host=alembic_settings.POSTGRES_HOST,
        port=alembic_settings.POSTGRES_PORT,
        database=alembic_settings.POSTGRES_DB,
    )


database_url = get_alembic_db_url()

config.set_main_option(
    "sqlalchemy.url",
    str(database_url)
)


def run_migrations_offline() -> None:
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

    connect_args = {}

    if alembic_settings.ENV == "production":
        connect_args = {
            "sslmode": "require"
        }

    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()