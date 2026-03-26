from redis.asyncio import Redis
from redis import RedisError
from typing import Dict, Any, List, Callable, Awaitable
import orjson
import asyncio
import random

from app.core.log.protocole import LoggerProtocol
from app.infra.cache.protocole import CacheProtocol
from app.infra.cache.exceptions import InternalCacheException

class RedisService(CacheProtocol):
    def __init__(
            self,
            cache_client: Redis,
            logger: LoggerProtocol
            ):
        self.client = cache_client
        self.logger = logger

    async def cache_set(
            self, 
            key: str, 
            data: Dict[str, Any] | List[Dict[str, Any]], 
            seconds: int | None = None
        ) -> bool | None:
        if not key:
            return False
        if not data:
           return False
        try:
            json_data = orjson.dumps(data)
            await self.client.set(name=key, ex=seconds, value=json_data, nx=True)
            return True
        except RedisError as r:
            raise InternalCacheException(
                "Cache set failed",
                {
                    "service": "redis/infra",
                    "key_name": key,
                    "event": "cache_set",
                }
            ) from r
    
    async def cache_get(self, key: str) -> Any | None:
        try:
            json_data = await self.client.get(key)
            if not json_data:
                return None
            result = orjson.loads(json_data)
            return result
        except RedisError as r:
            raise InternalCacheException(
                "Cache get failed",
                {
                    "service": "redis/infra",
                    "key_name": key,
                    "event": "cache_get",
                }
            ) from r

    async def cache_delete(self, key: str) -> bool:
        try:
            delete = await self.client.delete(key)
            if not delete:
                return False

            return True
        except RedisError as r:
            raise InternalCacheException(
                "Cache delete failed",
                {
                    "service": "redis/infra",
                    "key_name": key,
                    "event": "cache_delete"
                }
            ) from r
        
    async def cache_set_lock(self, key: str, seconds: int = 5) -> bool:
        lock_key: str = f"lock:{key}"
        try:
            return await self.client.set(name=lock_key, value="1", ex=seconds, nx=True)
        except RedisError as e:
            self.logger.exception("Redis set lock failed", key_name=lock_key, event="cache_set_lock")
            raise InternalCacheException(
                "Redis set lock failed",
                {
                    "service": "redis/infra",
                    "key_name": key,
                    "event": "cache_set_lock"
                }
            ) from e
        
    async def get_or_set_with_lock(
            self,
            key: str,
            ttl: int,
            callback: Callable[..., Awaitable[Any] | Any],
            kwargs: dict,
            lock_ttl: int = 5,
    ) -> Any:
        try:
            cached = await self.cache_get(key)
            if cached is not None:
                return cached
        
            if (await self.client.set(name=f"lock:{key}", value="1", ex=lock_ttl, nx=True)):
                data = await callback(**kwargs)

                await self.cache_set(
                    key=key,
                    data=data,
                    seconds=ttl
                )
                return data
        
            cached = await self.cache_retry_get(key, 5, delay=0.1)
            if cached is not None: return cached

            data = await callback(**kwargs)

            await self.cache_set(
                key=key,
                data=data,
                seconds=ttl
            )

            return data
        except RedisError as e:
            raise InternalCacheException(
                "Redis set lock failed",
                {
                    "service": "redis/infra",
                    "key_name": key,
                    "event": "cache_get_or_set_with_lock",
                    "lock_ttl": lock_ttl,
                    "ttl": ttl,
                    "kwargs": kwargs,
                    "action_name": callback.__name__
                }
            ) from e
        
    async def cache_retry_get(
            self,  
            key: str, 
            retries: int = 5,
            delay: float = 0.1
        ) -> Any | None:
        for attempt in range(retries):
            data = await self.client.get(key)

            if data is not None:
                return orjson.loads(data)

            if attempt < retries - 1:
                jitter = random.uniform(delay * 0.5, delay * 1.5)
                await asyncio.sleep(jitter)
        return None

    async def invalidate_family(self, key: str) -> None:
        cursor = 0

        while True:
            cursor, keys = await self.client.scan(cursor=cursor, match=key, count=100)
            if keys:
                async with self.client.pipeline() as pipe:
                    for k in keys:
                        pipe.delete(k)
                    await pipe.execute()
            if cursor == 0:
                break