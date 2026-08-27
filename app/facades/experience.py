from sqlalchemy.ext.asyncio import AsyncSession

from models import CVExperience
from schemas import (
    CVExperienceCreate,
    CVExperienceUpdate,
)
from services import CVExperienceService


class CVExperienceFacade:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.service = CVExperienceService(
            session
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVExperienceCreate,
    ) -> CVExperience:
        return await self.service.create(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def get_by_id(
        self,
        experience_id: int,
        user_id: int,
    ) -> CVExperience:
        return await self.service.get_by_id(
            experience_id=experience_id,
            user_id=user_id,
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> list[CVExperience]:
        return await self.service.get_by_cv_id(
            cv_id=cv_id,
            user_id=user_id,
        )

    async def update(
        self,
        experience_id: int,
        user_id: int,
        data: CVExperienceUpdate,
    ) -> CVExperience:
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
        await self.service.delete(
            experience_id=experience_id,
            user_id=user_id,
        )