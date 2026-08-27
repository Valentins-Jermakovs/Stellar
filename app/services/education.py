from sqlalchemy.ext.asyncio import AsyncSession

from models import CVEducation
from repositories import CVEducationRepository
from schemas import (
    CVEducationCreate,
    CVEducationUpdate,
)

from .ownership import CVOwnershipService


class CVEducationService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = CVEducationRepository(
            session
        )

        self.ownership = CVOwnershipService(
            session
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVEducationCreate,
    ) -> CVEducation:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        education = CVEducation(
            cv_id=cv_id,
            **data.model_dump(),
        )

        return await self.repository.create(
            education
        )

    async def get_by_id(
        self,
        education_id: int,
        user_id: int,
    ) -> CVEducation:
        await self.ownership.verify_education(
            education_id,
            user_id,
        )

        return await self.repository.get_by_id(
            education_id
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> list[CVEducation]:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        return await self.repository.get_by_cv_id(
            cv_id
        )

    async def update(
        self,
        education_id: int,
        user_id: int,
        data: CVEducationUpdate,
    ) -> CVEducation:
        education = await self.get_by_id(
            education_id,
            user_id,
        )

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(
                education,
                field,
                value,
            )

        return await self.repository.update(
            education
        )

    async def delete(
        self,
        education_id: int,
        user_id: int,
    ) -> None:
        education = await self.get_by_id(
            education_id,
            user_id,
        )

        await self.repository.delete(
            education
        )