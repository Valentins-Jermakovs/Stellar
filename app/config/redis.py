# ==============================
# Library Imports
# ==============================

from redis.asyncio import Redis


# ==============================
# Application Imports
# ==============================

from app.config.settings import settings


# ==============================
# Redis Client
# ==============================

# Redis client initialized during application startup.
redis: Redis | None = None


# ==============================
# Redis Lifecycle
# ==============================

async def init_redis() -> None:
    """Initialize Redis and verify the connection."""

    global redis

    # Reuse the existing client if it is still available.
    if redis is not None:
        try:
            await redis.ping()
            return
        except Exception:
            await redis.aclose()
            redis = None

    # Create a new Redis client.
    client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD or None,
        decode_responses=True,
    )

    # Verify the connection before storing the client.
    try:
        await client.ping()
    except Exception:
        await client.aclose()
        raise

    redis = client


# ==============================
# Redis Access
# ==============================

async def get_redis() -> Redis:
    """Return the initialized Redis client."""

    if redis is None:
        raise RuntimeError(
            "Redis has not been initialized."
        )

    return redis


# ==============================
# Redis Shutdown
# ==============================

async def close_redis() -> None:
    """Close the Redis connection and release the client."""

    global redis

    client = redis
    redis = None

    if client is not None:
        await client.aclose()