# Async database session and Redis client used by the service.
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

# Model and schemas used by the facade.
from app.models import CVProject
from app.schemas import (
    CVProjectCreate,
    CVProjectUpdate,
)

from app.services import CVProjectService


class CVProjectFacade:
    """Provide a simplified interface for CV project operations."""

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the facade with service dependencies."""
        self.service = CVProjectService(
            session=session,
            redis=redis,
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVProjectCreate,
    ) -> CVProject:
        """Create a project for a CV."""
        return await self.service.create(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def update(
        self,
        project_id: int,
        user_id: int,
        data: CVProjectUpdate,
    ) -> CVProject:
        """Update an existing project."""
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
        """Delete an existing project."""
        await self.service.delete(
            project_id=project_id,
            user_id=user_id,
        )