from app.infra.cache.redis_service import RedisService

from app.core.log.protocole import LoggerProtocol
from app.core.log.loguru_service import get_logger_service
from app.infra.cache.config import get_redis_client

from redis.asyncio import Redis
from fastapi import Depends

def get_cache_service(
    cache_client: Redis = Depends(get_redis_client),
    logger: LoggerProtocol = Depends(get_logger_service)
) -> RedisService:
    return RedisService(
        cache_client=cache_client,
        logger=logger
    )