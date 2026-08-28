from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVProject
from app.repositories import (
    CacheRepository,
    CVProjectRepository,
)
from app.schemas import (
    CVProjectCreate,
    CVProjectUpdate,
)
from app.utils import DataNormalizer

from .ownership import CVOwnershipService


class CVProjectService:
    """Handle projects associated with a CV."""

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the service dependencies."""
        self.session = session

        self.repository = CVProjectRepository(
            session
        )

        self.ownership = CVOwnershipService(
            session
        )

        self.cache = CacheRepository(
            redis
        )

    def _detail_cache_key(
        self,
        cv_id: int,
    ) -> str:
        """Build the cache key for a CV detail."""
        return f"cv:{cv_id}:detail"

    async def _invalidate_cv_cache(
        self,
        cv_id: int,
    ) -> None:
        """Remove the cached CV detail."""
        await self.cache.delete(
            self._detail_cache_key(
                cv_id
            )
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVProjectCreate,
    ) -> CVProject:
        """Create a project for a CV."""
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        values = DataNormalizer.normalize_model(
            data
        )

        existing = await self.repository.get_duplicate(
            cv_id=cv_id,
            name=values["name"],
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="This project already exists",
            )

        project = CVProject(
            cv_id=cv_id,
            **values,
        )

        await self.repository.create(
            project
        )

        await self.session.commit()
        await self.session.refresh(
            project
        )

        await self._invalidate_cv_cache(
            cv_id
        )

        return project

    async def update(
        self,
        project_id: int,
        user_id: int,
        data: CVProjectUpdate,
    ) -> CVProject:
        """Update an existing project."""
        project = await self.repository.get_by_id(
            project_id
        )

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )

        await self.ownership.verify_project(
            project_id,
            user_id,
        )

        values = DataNormalizer.normalize_model(
            data,
            exclude_unset=True,
        )

        new_name = values.get(
            "name",
            project.name,
        )

        existing = await self.repository.get_duplicate(
            cv_id=project.cv_id,
            name=new_name,
            exclude_id=project_id,
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="This project already exists",
            )

        for field, value in values.items():
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

        await self._invalidate_cv_cache(
            project.cv_id
        )

        return project

    async def delete(
        self,
        project_id: int,
        user_id: int,
    ) -> None:
        """Delete an existing project."""
        project = await self.repository.get_by_id(
            project_id
        )

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )

        await self.ownership.verify_project(
            project_id,
            user_id,
        )

        cv_id = project.cv_id

        await self.repository.delete(
            project
        )

        await self.session.commit()

        await self._invalidate_cv_cache(
            cv_id
        )