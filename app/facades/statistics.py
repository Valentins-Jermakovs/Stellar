# ==============================
# Library imports
# ==============================

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


# ==============================
# Application imports
# ==============================

from app.schemas import CVStatistics
from app.services import StatisticsService


# ==============================
# Statistics facade
# ==============================

class StatisticsFacade:
    """
    Provide a simplified interface for CV statistics.
    """

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """
        Initialize the facade with service dependencies.
        """

        self.service = StatisticsService(
            session=session,
            redis=redis,
        )

    async def get_user_statistics(
        self,
        user_id: int,
    ) -> CVStatistics:
        """
        Return statistics for the current user.
        """

        return await self.service.get_user_statistics(
            user_id
        )