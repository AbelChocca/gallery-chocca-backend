import pytest_asyncio

from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from app.infra.db.uow.dependency import get_uow
from app.infra.db.uow.unit_of_work import UnitOfWork
from tests.config.db_test import (
    async_session_factory,
)

@pytest_asyncio.fixture(
    scope="session",
    loop_scope="session",
)
async def http_client():

    from app.main import app

    async def override_get_uow():
        async with UnitOfWork(
            session_factory=async_session_factory,
        ) as uow:
            yield uow

    app.dependency_overrides[
        get_uow
    ] = override_get_uow

    async with LifespanManager(app):

        transport = ASGITransport(
            app=app,
        )

        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:

            yield client

    app.dependency_overrides.pop(
        get_uow,
        None,
    )