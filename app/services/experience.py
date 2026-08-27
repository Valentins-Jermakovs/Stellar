from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVExperience
from app.repositories import CVExperienceRepository
from app.schemas import (
    CVExperienceCreate,
    CVExperienceUpdate,
)

from .ownership import CVOwnershipService


class CVExperienceService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

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

        await self.repository.create(
            experience
        )

        await self.session.commit()

        await self.session.refresh(
            experience
        )

        return experience

    async def get_by_id(
        self,
        experience_id: int,
        user_id: int,
    ) -> CVExperience:
        await self.ownership.verify_experience(
            experience_id,
            user_id,
        )

        experience = await self.repository.get_by_id(
            experience_id
        )

        if experience is None:
            raise HTTPException(
                status_code=404,
                detail="Experience not found",
            )

        return experience

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

        await self.repository.update(
            experience
        )

        await self.session.commit()

        await self.session.refresh(
            experience
        )

        return experience

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

        await self.session.commit()