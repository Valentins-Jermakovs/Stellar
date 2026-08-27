from sqlalchemy.ext.asyncio import AsyncSession

from models import CVPersonalInfo
from repositories import CVPersonalInfoRepository
from schemas import (
    CVPersonalInfoCreate,
    CVPersonalInfoUpdate,
)

from .ownership import CVOwnershipService


class CVPersonalInfoService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = CVPersonalInfoRepository(
            session
        )

        self.ownership = CVOwnershipService(
            session
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVPersonalInfoCreate,
    ) -> CVPersonalInfo:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        existing = await self.repository.get_by_cv_id(
            cv_id
        )

        if existing is not None:
            raise ValueError(
                "Personal information already exists"
            )

        personal_info = CVPersonalInfo(
            cv_id=cv_id,
            **data.model_dump(),
        )

        return await self.repository.create(
            personal_info
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> CVPersonalInfo | None:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        return await self.repository.get_by_cv_id(
            cv_id
        )

    async def update(
        self,
        cv_id: int,
        user_id: int,
        data: CVPersonalInfoUpdate,
    ) -> CVPersonalInfo:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        personal_info = (
            await self.repository.get_by_cv_id(cv_id)
        )

        if personal_info is None:
            raise ValueError(
                "Personal information not found"
            )

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(
                personal_info,
                field,
                value,
            )

        return await self.repository.update(
            personal_info
        )

    async def delete(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        personal_info = (
            await self.repository.get_by_cv_id(cv_id)
        )

        if personal_info is not None:
            await self.repository.delete(
                personal_info
            )