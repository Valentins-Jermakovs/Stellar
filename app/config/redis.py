# Async Redis client used by the application.
from redis.asyncio import Redis

from .settings import settings


# Redis client is created during application startup.
# Until then, it remains uninitialized.
redis: Redis | None = None


async def init_redis() -> None:
    """Initialize the Redis client using application settings."""
    global redis

    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
    )


async def get_redis() -> Redis:
    """Return the initialized Redis client."""
    if redis is None:
        raise RuntimeError(
            "Redis has not been initialized"
        )

    return redis


async def close_redis() -> None:
    """Close the Redis connection and release the client."""
    global redis

    if redis is not None:
        await redis.aclose()
        redis = None

