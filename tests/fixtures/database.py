import pytest_asyncio

from sqlmodel import SQLModel
from sqlalchemy import text

from tests.config.db_test import (
    engine,
    async_session_factory,
)
from app.infra.db.uow.unit_of_work import UnitOfWork
from app.infra.db import model_registry  # noqa: F401


@pytest_asyncio.fixture(
    scope="session",
    loop_scope="session",
    autouse=True,
)
async def setup_database():

    async with engine.begin() as conn:

        await conn.execute(
            text(
                "CREATE EXTENSION IF NOT EXISTS pg_trgm"
            )
        )

        await conn.execute(
            text(
                "CREATE EXTENSION IF NOT EXISTS unaccent"
            )
        )

        await conn.run_sync(
            SQLModel.metadata.drop_all
        )

        await conn.run_sync(
            SQLModel.metadata.create_all
        )

        await conn.execute(
            text(
                """
                CREATE SEQUENCE IF NOT EXISTS complaint_number_seq
                AS BIGINT
                START WITH 1
                INCREMENT BY 1
                """
            )
        )

    yield

    async with engine.begin() as conn:
        await conn.run_sync(
            SQLModel.metadata.drop_all
        )

        await conn.execute(
            text(
                "DROP SEQUENCE IF EXISTS complaint_number_seq"
            )
        )


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
    autouse=True,
)
async def clean_database(
    setup_database,
):

    table_names = [
        f'"{table.name}"'
        for table in reversed(
            SQLModel.metadata.sorted_tables
        )
    ]

    if table_names:
        async with engine.connect() as conn:

            await conn.execute(
                text(
                    "TRUNCATE TABLE "
                    + ", ".join(table_names)
                    + " RESTART IDENTITY CASCADE"
                )
            )

            await conn.commit()

        async with engine.begin() as conn:
            await conn.execute(
                text(
                    "ALTER SEQUENCE complaint_number_seq RESTART WITH 1"
                )
            )

    yield


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def db_session():

    async with async_session_factory() as session:
        yield session

@pytest_asyncio.fixture
def uow_factory(db_session):
    def create_uow():
        return UnitOfWork(lambda: db_session)

    return create_uow