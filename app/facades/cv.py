from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.schemas import (
    CVCreate,
    CVDetailRead,
    CVPageRead,
    CVRead,
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

    # ==========================================
    # Create
    # ==========================================

    async def create(
        self,
        user_id: int,
        data: CVCreate,
    ) -> CVRead:
        return await self.service.create(
            user_id=user_id,
            data=data,
        )

    # ==========================================
    # Get Detail
    # ==========================================

    async def get_by_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> CVDetailRead:
        return await self.service.get_by_id(
            cv_id=cv_id,
            user_id=user_id,
        )

    # ==========================================
    # Search
    # ==========================================

    async def search(
        self,
        user_id: int,
        query: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> CVPageRead:
        return await self.service.search(
            user_id=user_id,
            query=query,
            page=page,
            page_size=page_size,
        )

    # ==========================================
    # Update
    # ==========================================

    async def update(
        self,
        cv_id: int,
        user_id: int,
        data: CVUpdate,
    ) -> CVRead:
        return await self.service.update(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    # ==========================================
    # Delete
    # ==========================================

    async def delete(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        await self.service.delete(
            cv_id=cv_id,
            user_id=user_id,
        )