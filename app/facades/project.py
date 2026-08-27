from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVProject
from app.schemas import (
    CVProjectCreate,
    CVProjectUpdate,
)
from app.services import CVProjectService


class CVProjectFacade:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.service = CVProjectService(
            session
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVProjectCreate,
    ) -> CVProject:
        return await self.service.create(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def get_by_id(
        self,
        project_id: int,
        user_id: int,
    ) -> CVProject:
        return await self.service.get_by_id(
            project_id=project_id,
            user_id=user_id,
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> list[CVProject]:
        return await self.service.get_by_cv_id(
            cv_id=cv_id,
            user_id=user_id,
        )

    async def update(
        self,
        project_id: int,
        user_id: int,
        data: CVProjectUpdate,
    ) -> CVProject:
        return await self.service.update(
            project_id=project_id,
            user_id=user_id,
            data=data,
        )

    async def delete(
        self,
        project_id: int,
        user_id: int,
    ) -> None:
        await self.service.delete(
            project_id=project_id,
            user_id=user_id,
        )