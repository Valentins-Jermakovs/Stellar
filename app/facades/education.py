# ==============================
# Library imports
# ==============================

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


# ==============================
# Application imports
# ==============================

from app.models import CVEducation

from app.schemas import (
    CVEducationCreate,
    CVEducationUpdate,
)

from app.services import CVEducationService


# ==============================
# CV education facade
# ==============================

class CVEducationFacade:
    """
    Provide a simplified interface for CV education operations.
    """

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """
        Initialize the facade with service dependencies.
        """

        self.service = CVEducationService(
            session=session,
            redis=redis,
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVEducationCreate,
    ) -> CVEducation:
        """
        Create an education entry for a CV.
        """

        return await self.service.create(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def update(
        self,
        education_id: int,
        user_id: int,
        data: CVEducationUpdate,
    ) -> CVEducation:
        """
        Update an existing education entry.
        """

        return await self.service.update(
            education_id=education_id,
            user_id=user_id,
            data=data,
        )

    async def delete(
        self,
        education_id: int,
        user_id: int,
    ) -> None:
        """
        Delete an existing education entry.
        """

        await self.service.delete(
            education_id=education_id,
            user_id=user_id,
        )