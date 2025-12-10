# app.tests.conftest.py
import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlmodel import SQLModel

from app.core.settings.test_pydantic_settings import test_settings

test_db_url =  test_settings.DATABASE_URL


@pytest_asyncio.fixture(scope='function')
async def engine():
    # Motor de base de datos de prueba
    engine_conn = create_async_engine(url=test_db_url)
    async with engine_conn.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine_conn
    async with engine_conn.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine_conn.dispose()

@pytest_asyncio.fixture
async def session(engine):
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

#@pytest_asyncio.fixture(name="client")
#async def client_fixture(session: AsyncSession, redis_client: RedisClient):
#
#    app.dependency_overrides[get_user_session] = mock_get_user_session
#    app.dependency_overrides[get_async_session] = lambda: session
#    app.dependency_overrides[get_user_repository] = lambda: user_repo
#    app.dependency_overrides[get_product_repository] = lambda: product_repo
#    app.dependency_overrides[get_redis_client] = lambda: redis_client
#
#    transport = ASGITransport(app=app)
#    async with AsyncClient(transport=transport, base_url="http://test") as client:
#        yield client
#
#    app.dependency_overrides.clear()
