from sqlalchemy.ext.asyncio import AsyncSession

from models import CVProject
from repositories import CVProjectRepository
from schemas import (
    CVProjectCreate,
    CVProjectUpdate,
)

from .ownership import CVOwnershipService


class CVProjectService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = CVProjectRepository(
            session
        )

        self.ownership = CVOwnershipService(
            session
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVProjectCreate,
    ) -> CVProject:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        project = CVProject(
            cv_id=cv_id,
            **data.model_dump(),
        )

        return await self.repository.create(
            project
        )

    async def get_by_id(
        self,
        project_id: int,
        user_id: int,
    ) -> CVProject:
        await self.ownership.verify_project(
            project_id,
            user_id,
        )

        return await self.repository.get_by_id(
            project_id
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> list[CVProject]:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        return await self.repository.get_by_cv_id(
            cv_id
        )

    async def update(
        self,
        project_id: int,
        user_id: int,
        data: CVProjectUpdate,
    ) -> CVProject:
        project = await self.get_by_id(
            project_id,
            user_id,
        )

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(
                project,
                field,
                value,
            )

        return await self.repository.update(
            project
        )

    async def delete(
        self,
        project_id: int,
        user_id: int,
    ) -> None:
        project = await self.get_by_id(
            project_id,
            user_id,
        )

        await self.repository.delete(
            project
        )