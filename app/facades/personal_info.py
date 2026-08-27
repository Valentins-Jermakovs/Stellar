from sqlalchemy.ext.asyncio import AsyncSession

from models import CVPersonalInfo
from schemas import (
    CVPersonalInfoCreate,
    CVPersonalInfoUpdate,
)
from services import CVPersonalInfoService


class CVPersonalInfoFacade:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.service = CVPersonalInfoService(
            session
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVPersonalInfoCreate,
    ) -> CVPersonalInfo:
        return await self.service.create(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> CVPersonalInfo | None:
        return await self.service.get_by_cv_id(
            cv_id=cv_id,
            user_id=user_id,
        )

    async def update(
        self,
        cv_id: int,
        user_id: int,
        data: CVPersonalInfoUpdate,
    ) -> CVPersonalInfo:
        return await self.service.update(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def delete(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        await self.service.delete(
            cv_id=cv_id,
            user_id=user_id,
        )