# ==============================
# Library imports
# ==============================

import json

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


# ==============================
# Application imports
# ==============================

from app.repositories import (
    CacheRepository,
    StatisticsRepository,
)
from app.schemas import CVStatistics


# ==============================
# Statistics service
# ==============================

class StatisticsService:
    """
    This class handles CV statistics operations.

    It retrieves aggregated user statistics and uses Redis
    to cache the results for a short period of time.
    """

    # Cache expiration time in seconds
    CACHE_EXPIRE = 60

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the service dependencies."""

        # Repository for statistics operations
        self.repository = StatisticsRepository(
            session
        )

        # Repository for Redis cache operations
        self.cache = CacheRepository(
            redis
        )

    def _get_cache_key(
        self,
        user_id: int,
    ) -> str:
        """Build the cache key for user statistics."""
        return f"statistics:user:{user_id}"

    async def get_user_statistics(
        self,
        user_id: int,
    ) -> CVStatistics:
        """
        Return aggregated statistics for the current user.

        Cached statistics are returned when available.
        Otherwise, the statistics are loaded from the database,
        cached in Redis, and returned to the caller.
        """
        cache_key = self._get_cache_key(
            user_id
        )

        cached = await self.cache.get(
            cache_key
        )

        if cached is not None:
            return CVStatistics(
                **json.loads(cached)
            )

        statistics = await self.repository.get_user_statistics(
            user_id
        )

        result = CVStatistics(
            **statistics
        )

        # Cache the serialized statistics for future requests
        await self.cache.set(
            cache_key,
            json.dumps(
                result.model_dump()
            ),
            expire=self.CACHE_EXPIRE,
        )

        return result