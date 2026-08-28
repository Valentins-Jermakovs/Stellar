# Async database session and Redis client used by the service.
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

# Model and schemas used by the facade.
from app.models import CVCertification
from app.schemas import (
    CVCertificationCreate,
    CVCertificationUpdate,
)

from app.services import CVCertificationService


class CVCertificationFacade:
    """Provide a simplified interface for CV certification operations."""

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the facade with service dependencies."""
        self.service = CVCertificationService(
            session=session,
            redis=redis,
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVCertificationCreate,
    ) -> CVCertification:
        """Create a certification for a CV."""
        return await self.service.create(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def update(
        self,
        certification_id: int,
        user_id: int,
        data: CVCertificationUpdate,
    ) -> CVCertification:
        """Update an existing certification."""
        return await self.service.update(
            certification_id=certification_id,
            user_id=user_id,
            data=data,
        )

    async def delete(
        self,
        certification_id: int,
        user_id: int,
    ) -> None:
        """Delete an existing certification."""
        await self.service.delete(
            certification_id=certification_id,
            user_id=user_id,
        )