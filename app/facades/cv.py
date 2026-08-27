from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.models import CV
from app.schemas import (
    CVCreate,
    CVUpdate,
)
from app.services import CVService


class CVFacade:
    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        self.service = CVService(
            session=session,
            redis=redis,
        )

    async def create(
        self,
        user_id: int,
        data: CVCreate,
    ) -> CV:
        return await self.service.create(
            user_id=user_id,
            data=data,
        )

    async def get_by_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> CV:
        return await self.service.get_by_id(
            cv_id=cv_id,
            user_id=user_id,
        )

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> list[CV]:
        return await self.service.get_by_user_id(
            user_id=user_id,
        )

    async def update(
        self,
        cv_id: int,
        user_id: int,
        data: CVUpdate,
    ) -> CV:
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