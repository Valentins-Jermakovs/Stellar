from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVCertification
from app.schemas import (
    CVCertificationCreate,
    CVCertificationUpdate,
)
from app.services import CVCertificationService


class CVCertificationFacade:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.service = CVCertificationService(
            session
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVCertificationCreate,
    ) -> CVCertification:
        return await self.service.create(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def get_by_id(
        self,
        certification_id: int,
        user_id: int,
    ) -> CVCertification:
        return await self.service.get_by_id(
            certification_id=certification_id,
            user_id=user_id,
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> list[CVCertification]:
        return await self.service.get_by_cv_id(
            cv_id=cv_id,
            user_id=user_id,
        )

    async def update(
        self,
        certification_id: int,
        user_id: int,
        data: CVCertificationUpdate,
    ) -> CVCertification:
        return await self.service.update(
            certification_id=certification_id,
            user_id=user_id,
            data=data,
        )

    async def delete(
        self,
        certification_id: int,
        user_id: int,
    ) -> None:
        await self.service.delete(
            certification_id=certification_id,
            user_id=user_id,
        )