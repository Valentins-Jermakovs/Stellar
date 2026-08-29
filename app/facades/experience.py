# ==============================
# Library imports
# ==============================

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


# ==============================
# Application imports
# ==============================

from app.models import CVExperience

from app.schemas import (
    CVExperienceCreate,
    CVExperienceUpdate,
)

from app.services import CVExperienceService


# ==============================
# CV experience facade
# ==============================

class CVExperienceFacade:
    """
    Provide a simplified interface for CV experience operations.
    """

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """
        Initialize the facade with service dependencies.
        """

        self.service = CVExperienceService(
            session=session,
            redis=redis,
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVExperienceCreate,
    ) -> CVExperience:
        """
        Create a work experience entry for a CV.
        """

        return await self.service.create(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def update(
        self,
        experience_id: int,
        user_id: int,
        data: CVExperienceUpdate,
    ) -> CVExperience:
        """
        Update an existing work experience entry.
        """

        return await self.service.update(
            experience_id=experience_id,
            user_id=user_id,
            data=data,
        )

    async def delete(
        self,
        experience_id: int,
        user_id: int,
    ) -> None:
        """
        Delete an existing work experience entry.
        """

        await self.service.delete(
            experience_id=experience_id,
            user_id=user_id,
        )