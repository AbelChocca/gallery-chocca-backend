from fastapi import Request, Depends, HTTPException, status
from redis.asyncio import Redis

from typing import Callable, Optional, Awaitable

from app.infra.cache.config import get_redis_client

class RateLimiter:
    def limiter(self, limit = 5, window = 60) -> Callable[[Request], Awaitable[Optional[HTTPException]]]:
        async def dependency(request: Request, redis_client: Redis = Depends(get_redis_client)) -> Optional[HTTPException]:
            key = f"rate:{request.client.host}:{request.url.path}"
            current = await redis_client.incr(key)
            if current == 1:
                await redis_client.expire(key, window)
            if current > limit:
                raise HTTPException(
                    detail={"message": f"Rate limit exceeded. Try again in {window} seconds."},
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS
                )
        return dependency
    
limiter = RateLimiter()