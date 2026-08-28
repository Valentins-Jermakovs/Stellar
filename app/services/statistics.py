import json

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import (
    CacheRepository,
    StatisticsRepository,
)
from app.schemas import CVStatistics


class StatisticsService:
    """Handle CV statistics operations."""

    CACHE_EXPIRE = 60

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the service dependencies."""
        self.repository = StatisticsRepository(
            session
        )

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
        """Return aggregated statistics for the current user."""
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

        await self.cache.set(
            cache_key,
            json.dumps(
                result.model_dump()
            ),
            expire=self.CACHE_EXPIRE,
        )

        return result

