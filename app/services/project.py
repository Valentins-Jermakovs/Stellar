from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVProject
from app.repositories import CVProjectRepository
from app.schemas import (
    CVProjectCreate,
    CVProjectUpdate,
)

from .ownership import CVOwnershipService


class CVProjectService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

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

        await self.repository.create(
            project
        )

        await self.session.commit()

        await self.session.refresh(
            project
        )

        return project

    async def get_by_id(
        self,
        project_id: int,
        user_id: int,
    ) -> CVProject:
        await self.ownership.verify_project(
            project_id,
            user_id,
        )

        project = await self.repository.get_by_id(
            project_id
        )

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )

        return project

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

        await self.repository.update(
            project
        )

        await self.session.commit()

        await self.session.refresh(
            project
        )

        return project

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

        await self.session.commit()