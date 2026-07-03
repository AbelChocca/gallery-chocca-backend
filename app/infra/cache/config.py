from fastapi import Request
from redis.asyncio import Redis

def get_redis_client(request: Request) -> Redis:
    return request.app.state.redis

