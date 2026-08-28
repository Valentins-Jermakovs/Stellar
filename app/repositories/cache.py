# Async Redis client used for cache operations.
from redis.asyncio import Redis


class CacheRepository:
    """Repository for Redis cache operations."""

    def __init__(self, redis: Redis):
        """Initialize the repository with a Redis client."""
        self.redis = redis

    async def get(self, key: str) -> str | None:
        """Return the cached value for a key, if it exists."""
        return await self.redis.get(key)

    async def set(
        self,
        key: str,
        value: str,
        expire: int | None = None,
    ) -> None:
        """Store a value in the cache with an optional expiration."""
        await self.redis.set(
            key,
            value,
            ex=expire,
        )

    async def delete(self, key: str) -> None:
        """Delete a value from the cache."""
        await self.redis.delete(key)

    async def delete_pattern(self, pattern: str) -> None:
        """Delete all keys matching the given pattern."""
        keys = await self.redis.keys(pattern)

        if keys:
            await self.redis.delete(
                *keys
            )

    async def exists(self, key: str) -> bool:
        """Return whether a key exists in the cache."""
        return bool(
            await self.redis.exists(key)
        )