from redis.asyncio import Redis

from .settings import settings


redis: Redis | None = None


async def init_redis() -> None:
    global redis

    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD or None,
        decode_responses=True,
    )


async def get_redis() -> Redis:
    if redis is None:
        raise RuntimeError(
            "Redis has not been initialized"
        )

    return redis


async def close_redis() -> None:
    global redis

    if redis is not None:
        await redis.aclose()
        redis = None