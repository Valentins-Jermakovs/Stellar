from sqlalchemy.ext.asyncio import AsyncSession

from models import CVEducation
from schemas import (
    CVEducationCreate,
    CVEducationUpdate,
)
from services import CVEducationService


class CVEducationFacade:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.service = CVEducationService(
            session
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVEducationCreate,
    ) -> CVEducation:
        return await self.service.create(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def get_by_id(
        self,
        education_id: int,
        user_id: int,
    ) -> CVEducation:
        return await self.service.get_by_id(
            education_id=education_id,
            user_id=user_id,
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> list[CVEducation]:
        return await self.service.get_by_cv_id(
            cv_id=cv_id,
            user_id=user_id,
        )

    async def update(
        self,
        education_id: int,
        user_id: int,
        data: CVEducationUpdate,
    ) -> CVEducation:
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
        await self.service.delete(
            education_id=education_id,
            user_id=user_id,
        )