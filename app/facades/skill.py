# Async database session and Redis client used by the services.
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

# Models and schemas used by the facades.
from app.models import CVSkill, Skill
from app.schemas import (
    CVSkillCreate,
    CVSkillUpdate,
    SkillCreate,
)

from app.services import (
    CVSkillService,
    SkillService,
)


class SkillFacade:
    """Provide a simplified interface for the global skill catalog."""

    def __init__(
        self,
        session: AsyncSession,
    ):
        """Initialize the facade with service dependencies."""
        self.service = SkillService(
            session
        )

    async def create(
        self,
        data: SkillCreate,
    ) -> Skill:
        """Create a skill or return an existing one."""
        return await self.service.create(
            data
        )

    async def get_by_id(
        self,
        skill_id: int,
    ) -> Skill:
        """Return a global skill by ID."""
        return await self.service.get_by_id(
            skill_id
        )

    async def search(
        self,
        query: str | None = None,
    ) -> list[Skill]:
        """Search the global skill catalog."""
        return await self.service.search(
            query
        )


class CVSkillFacade:
    """Provide a simplified interface for CV skill operations."""

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the facade with service dependencies."""
        self.service = CVSkillService(
            session=session,
            redis=redis,
        )

    async def add(
        self,
        cv_id: int,
        user_id: int,
        data: CVSkillCreate,
    ) -> CVSkill:
        """Add a skill to a CV."""
        return await self.service.add(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def update(
        self,
        cv_id: int,
        user_id: int,
        skill_id: int,
        data: CVSkillUpdate,
    ) -> CVSkill:
        """Update a skill association in a CV."""
        return await self.service.update(
            cv_id=cv_id,
            user_id=user_id,
            skill_id=skill_id,
            data=data,
        )

    async def delete(
        self,
        cv_id: int,
        user_id: int,
        skill_id: int,
    ) -> None:
        """Delete a skill association from a CV."""
        await self.service.delete(
            cv_id=cv_id,
            user_id=user_id,
            skill_id=skill_id,
        )