from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVCertification
from app.repositories import CVCertificationRepository
from app.schemas import (
    CVCertificationCreate,
    CVCertificationUpdate,
)

from .ownership import CVOwnershipService


class CVCertificationService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = CVCertificationRepository(
            session
        )

        self.ownership = CVOwnershipService(
            session
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVCertificationCreate,
    ) -> CVCertification:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        certification = CVCertification(
            cv_id=cv_id,
            **data.model_dump(),
        )

        return await self.repository.create(
            certification
        )

    async def get_by_id(
        self,
        certification_id: int,
        user_id: int,
    ) -> CVCertification:
        await self.ownership.verify_certification(
            certification_id,
            user_id,
        )

        return await self.repository.get_by_id(
            certification_id
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> list[CVCertification]:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        return await self.repository.get_by_cv_id(
            cv_id
        )

    async def update(
        self,
        certification_id: int,
        user_id: int,
        data: CVCertificationUpdate,
    ) -> CVCertification:
        certification = await self.get_by_id(
            certification_id,
            user_id,
        )

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(
                certification,
                field,
                value,
            )

        return await self.repository.update(
            certification
        )

    async def delete(
        self,
        certification_id: int,
        user_id: int,
    ) -> None:
        certification = await self.get_by_id(
            certification_id,
            user_id,
        )

        await self.repository.delete(
            certification
        )