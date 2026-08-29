# ==============================
# Library imports
# ==============================

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


# ==============================
# Application imports
# ==============================

from app.models import CVPersonalInfo

from app.schemas import (
    CVPersonalInfoCreate,
    CVPersonalInfoUpdate,
)

from app.services import CVPersonalInfoService


# ==============================
# CV personal information facade
# ==============================

class CVPersonalInfoFacade:
    """
    Provide a simplified interface for CV personal information.
    """

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """
        Initialize the facade with service dependencies.
        """

        self.service = CVPersonalInfoService(
            session=session,
            redis=redis,
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVPersonalInfoCreate,
    ) -> CVPersonalInfo:
        """
        Create personal information for a CV.
        """

        return await self.service.create(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def update(
        self,
        cv_id: int,
        user_id: int,
        data: CVPersonalInfoUpdate,
    ) -> CVPersonalInfo:
        """
        Update personal information for a CV.
        """

        return await self.service.update(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def delete(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        """
        Delete personal information from a CV.
        """

        await self.service.delete(
            cv_id=cv_id,
            user_id=user_id,
        )