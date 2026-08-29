# ==============================
# Library imports
# ==============================

from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


# ==============================
# Application imports
# ==============================

from app.models import CVSkill, Skill
from app.repositories import (
    CacheRepository,
    CVSkillRepository,
    SkillRepository,
)
from app.schemas import (
    CVSkillCreate,
    CVSkillUpdate,
    SkillCreate,
)
from app.utils import DataNormalizer

from .ownership import CVOwnershipService


# ==============================
# Global skill service
# ==============================

class SkillService:
    """
    This class handles operations with the global skill catalog.

    It provides methods for creating, retrieving, and searching
    skills that can be reused across multiple CVs.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        """Initialize the service dependencies."""
        self.session = session

        # Repository for global skill operations
        self.repository = SkillRepository(
            session
        )

    async def create(
        self,
        data: SkillCreate,
    ) -> Skill:
        """Create a skill or return an existing one."""
        values = DataNormalizer.normalize_model(
            data
        )

        existing = await self.repository.get_by_name(
            values["name"]
        )

        if existing is not None:
            return existing

        skill = Skill(
            name=values["name"]
        )

        await self.repository.create(
            skill
        )

        await self.session.commit()
        await self.session.refresh(
            skill
        )

        return skill

    async def get_by_id(
        self,
        skill_id: int,
    ) -> Skill:
        """Return a global skill by its ID."""
        skill = await self.repository.get_by_id(
            skill_id
        )

        if skill is None:
            raise HTTPException(
                status_code=404,
                detail="Skill not found",
            )

        return skill

    async def search(
        self,
        query: str | None = None,
    ) -> list[Skill]:
        """Return up to ten global skills matching the query."""
        if query is not None:
            query = DataNormalizer.normalize_string(
                query
            )

            if not query:
                query = None

        return await self.repository.search(
            query=query,
            limit=10,
        )


# ==============================
# CV skill service
# ==============================

class CVSkillService:
    """
    This class handles skills associated with a CV.

    It provides methods for adding, updating, and removing skills,
    while also validating CV ownership and maintaining the cache.
    """

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the service dependencies."""
        self.session = session

        # Repository for CV skill associations
        self.repository = CVSkillRepository(
            session
        )

        # Repository for global skill operations
        self.skill_repository = SkillRepository(
            session
        )

        # Service for CV ownership validation
        self.ownership = CVOwnershipService(
            session
        )

        # Repository for Redis cache operations
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

    async def add(
        self,
        cv_id: int,
        user_id: int,
        data: CVSkillCreate,
    ) -> CVSkill:
        """Add a global skill to a CV."""
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        skill = await self.skill_repository.get_by_id(
            data.skill_id
        )

        if skill is None:
            raise HTTPException(
                status_code=404,
                detail="Skill not found",
            )

        existing = await self.repository.get(
            cv_id,
            data.skill_id,
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="Skill already added to CV",
            )

        values = DataNormalizer.normalize_model(
            data
        )

        cv_skill = CVSkill(
            cv_id=cv_id,
            **values,
        )

        await self.repository.create(
            cv_skill
        )

        await self.session.commit()

        # Invalidate cached CV data after modification
        await self._invalidate_cv_cache(
            cv_id
        )

        return cv_skill

    async def update(
        self,
        cv_id: int,
        user_id: int,
        skill_id: int,
        data: CVSkillUpdate,
    ) -> CVSkill:
        """Update a skill association in a CV."""
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        cv_skill = await self.repository.get(
            cv_id,
            skill_id,
        )

        if cv_skill is None:
            raise HTTPException(
                status_code=404,
                detail="CV skill not found",
            )

        values = DataNormalizer.normalize_model(
            data,
            exclude_unset=True,
        )

        for field, value in values.items():
            setattr(
                cv_skill,
                field,
                value,
            )

        await self.repository.update(
            cv_skill
        )

        await self.session.commit()
        await self.session.refresh(
            cv_skill
        )

        # Invalidate cached CV data after modification
        await self._invalidate_cv_cache(
            cv_id
        )

        return cv_skill

    async def delete(
        self,
        cv_id: int,
        user_id: int,
        skill_id: int,
    ) -> None:
        """Remove a skill association from a CV."""
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        cv_skill = await self.repository.get(
            cv_id,
            skill_id,
        )

        if cv_skill is None:
            raise HTTPException(
                status_code=404,
                detail="CV skill not found",
            )

        await self.repository.delete(
            cv_skill
        )

        await self.session.commit()

        # Invalidate cached CV data after modification
        await self._invalidate_cv_cache(
            cv_id
        )