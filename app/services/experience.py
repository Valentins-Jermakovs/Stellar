from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVExperience
from app.repositories import (
    CacheRepository,
    CVExperienceRepository,
)
from app.schemas import (
    CVExperienceCreate,
    CVExperienceUpdate,
)
from app.utils import DataNormalizer

from .ownership import CVOwnershipService


class CVExperienceService:
    """Handle work experience entries associated with a CV."""

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the service dependencies."""
        self.session = session

        self.repository = CVExperienceRepository(
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
        data: CVExperienceCreate,
    ) -> CVExperience:
        """Create a work experience entry for a CV."""
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        values = DataNormalizer.normalize_model(
            data
        )

        # Check whether the same experience already exists in this CV.
        existing = await self.repository.get_duplicate(
            cv_id=cv_id,
            company=values["company"],
            position=values["position"],
            start_date=values["start_date"],
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="This work experience already exists",
            )

        experience = CVExperience(
            cv_id=cv_id,
            **values,
        )

        await self.repository.create(
            experience
        )

        await self.session.commit()
        await self.session.refresh(
            experience
        )

        await self._invalidate_cv_cache(
            cv_id
        )

        return experience

    async def update(
        self,
        experience_id: int,
        user_id: int,
        data: CVExperienceUpdate,
    ) -> CVExperience:
        """Update an existing work experience entry."""
        await self.ownership.verify_experience(
            experience_id,
            user_id,
        )

        experience = await self.repository.get_by_id(
            experience_id
        )

        if experience is None:
            raise HTTPException(
                status_code=404,
                detail="Experience not found",
            )

        values = DataNormalizer.normalize_model(
            data,
            exclude_unset=True,
        )

        # Use existing values for fields that were not provided.
        company = values.get(
            "company",
            experience.company,
        )

        position = values.get(
            "position",
            experience.position,
        )

        start_date = values.get(
            "start_date",
            experience.start_date,
        )

        # Ignore the current entry when checking for duplicates.
        existing = await self.repository.get_duplicate(
            cv_id=experience.cv_id,
            company=company,
            position=position,
            start_date=start_date,
            exclude_id=experience_id,
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="This work experience already exists",
            )

        for field, value in values.items():
            setattr(
                experience,
                field,
                value,
            )

        await self.repository.update(
            experience
        )

        await self.session.commit()
        await self.session.refresh(
            experience
        )

        await self._invalidate_cv_cache(
            experience.cv_id
        )

        return experience

    async def delete(
        self,
        experience_id: int,
        user_id: int,
    ) -> None:
        """Delete an existing work experience entry."""
        await self.ownership.verify_experience(
            experience_id,
            user_id,
        )

        experience = await self.repository.get_by_id(
            experience_id
        )

        if experience is None:
            raise HTTPException(
                status_code=404,
                detail="Experience not found",
            )

        cv_id = experience.cv_id

        await self.repository.delete(
            experience
        )

        await self.session.commit()

        await self._invalidate_cv_cache(
            cv_id
        )