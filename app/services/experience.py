from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models import CVExperience
from repositories import CVExperienceRepository
from schemas import (
    CVExperienceCreate,
    CVExperienceUpdate,
)

from .ownership import CVOwnershipService


class CVExperienceService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = CVExperienceRepository(
            session
        )

        self.ownership = CVOwnershipService(
            session
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVExperienceCreate,
    ) -> CVExperience:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        experience = CVExperience(
            cv_id=cv_id,
            **data.model_dump(),
        )

        return await self.repository.create(
            experience
        )

    async def get_by_id(
        self,
        experience_id: int,
        user_id: int,
    ) -> CVExperience:
        await self.ownership.verify_experience(
            experience_id,
            user_id,
        )

        return await self.repository.get_by_id(
            experience_id
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> list[CVExperience]:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        return await self.repository.get_by_cv_id(
            cv_id
        )

    async def update(
        self,
        experience_id: int,
        user_id: int,
        data: CVExperienceUpdate,
    ) -> CVExperience:
        experience = await self.get_by_id(
            experience_id,
            user_id,
        )

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(
                experience,
                field,
                value,
            )

        return await self.repository.update(
            experience
        )

    async def delete(
        self,
        experience_id: int,
        user_id: int,
    ) -> None:
        experience = await self.get_by_id(
            experience_id,
            user_id,
        )

        await self.repository.delete(
            experience
        )