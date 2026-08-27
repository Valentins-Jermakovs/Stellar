from redis.asyncio import Redis

from .settings import settings


redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD or None,
    decode_responses=True,
)


async def get_redis() -> Redis:
    return redis


async def close_redis() -> None:
    await redis.aclose()