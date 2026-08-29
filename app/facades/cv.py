# ==============================
# Library imports
# ==============================

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


# ==============================
# Application imports
# ==============================

from app.schemas import (
    CVCreate,
    CVDetailRead,
    CVPageRead,
    CVRead,
    CVUpdate,
)

from app.services import CVService


# ==============================
# CV facade
# ==============================

class CVFacade:
    """
    Provide a simplified interface for CV operations.
    """

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """
        Initialize the facade with service dependencies.
        """

        self.service = CVService(
            session=session,
            redis=redis,
        )

    async def create(
        self,
        user_id: int,
        data: CVCreate,
    ) -> CVRead:
        """
        Create a new CV for a user.
        """

        return await self.service.create(
            user_id=user_id,
            data=data,
        )

    async def get_by_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> CVDetailRead:
        """
        Return a CV with all related data.
        """

        return await self.service.get_by_id(
            cv_id=cv_id,
            user_id=user_id,
        )

    async def search(
        self,
        user_id: int,
        query: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> CVPageRead:
        """
        Search a user's CVs with pagination.
        """

        return await self.service.search(
            user_id=user_id,
            query=query,
            page=page,
            page_size=page_size,
        )

    async def update(
        self,
        cv_id: int,
        user_id: int,
        data: CVUpdate,
    ) -> CVRead:
        """
        Update a user's CV.
        """

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
        """
        Delete a user's CV.
        """

        await self.service.delete(
            cv_id=cv_id,
            user_id=user_id,
        )