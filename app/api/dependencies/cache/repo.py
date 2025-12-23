from app.modules.cache.cache_repository import CacheRepository
from app.modules.cache.redis_cache_repository import RedisCacheRepository

from app.core.log.logger_repository import LoggerRepository
from app.core.log.loguru_logger_repository import get_logger_repo
from app.core.clients.redis_client import get_redis_client

from redis.asyncio import Redis
from fastapi import Depends


def get_cache_repo(
    cache_client: Redis = Depends(get_redis_client),
    logger: LoggerRepository = Depends(get_logger_repo)
) -> CacheRepository:
    return RedisCacheRepository(
        cache_client=cache_client,
        logger=logger
    )