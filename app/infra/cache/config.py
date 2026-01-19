from redis.asyncio import from_url, Redis
from functools import lru_cache

from app.core.settings.pydantic_settings import settings

@lru_cache
def get_redis_client() -> Redis:
    """
    Returns a singleton Redis client using asyncio.
    """
    return from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True
    )

