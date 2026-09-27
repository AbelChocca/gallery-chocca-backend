import pytest_asyncio
import redis.asyncio as redis

from app.core.settings.pydantic_test_settings import (
    test_settings,
)


@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
    autouse=True,
)
async def clean_test_redis():

    client = redis.from_url(
        test_settings.REDIS_URL,
        decode_responses=True,
    )

    await client.flushdb()

    yield

    await client.aclose()