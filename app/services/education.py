from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVEducation
from app.repositories import (
    CacheRepository,
    CVEducationRepository,
)
from app.schemas import (
    CVEducationCreate,
    CVEducationUpdate,
)
from app.utils import DataNormalizer

from .ownership import CVOwnershipService


class CVEducationService:
    """Handle education entries associated with a CV."""

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the service dependencies."""
        self.session = session

        self.repository = CVEducationRepository(
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
        data: CVEducationCreate,
    ) -> CVEducation:
        """Create an education entry for a CV."""
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        values = DataNormalizer.normalize_model(
            data
        )

        # Check whether the same education entry already exists in this CV.
        existing = await self.repository.get_duplicate(
            cv_id=cv_id,
            institution=values["institution"],
            degree=values.get("degree"),
            field_of_study=values.get("field_of_study"),
            start_date=values.get("start_date"),
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="This education entry already exists",
            )

        education = CVEducation(
            cv_id=cv_id,
            **values,
        )

        await self.repository.create(
            education
        )

        await self.session.commit()
        await self.session.refresh(
            education
        )

        await self._invalidate_cv_cache(
            cv_id
        )

        return education

    async def update(
        self,
        education_id: int,
        user_id: int,
        data: CVEducationUpdate,
    ) -> CVEducation:
        """Update an existing education entry."""
        await self.ownership.verify_education(
            education_id,
            user_id,
        )

        education = await self.repository.get_by_id(
            education_id
        )

        if education is None:
            raise HTTPException(
                status_code=404,
                detail="Education not found",
            )

        values = DataNormalizer.normalize_model(
            data,
            exclude_unset=True,
        )

        # Use existing values for fields that were not provided.
        institution = values.get(
            "institution",
            education.institution,
        )

        degree = values.get(
            "degree",
            education.degree,
        )

        field_of_study = values.get(
            "field_of_study",
            education.field_of_study,
        )

        start_date = values.get(
            "start_date",
            education.start_date,
        )

        # Ignore the current entry when checking for duplicates.
        existing = await self.repository.get_duplicate(
            cv_id=education.cv_id,
            institution=institution,
            degree=degree,
            field_of_study=field_of_study,
            start_date=start_date,
            exclude_id=education_id,
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="This education entry already exists",
            )

        for field, value in values.items():
            setattr(
                education,
                field,
                value,
            )

        await self.repository.update(
            education
        )

        await self.session.commit()
        await self.session.refresh(
            education
        )

        await self._invalidate_cv_cache(
            education.cv_id
        )

        return education

    async def delete(
        self,
        education_id: int,
        user_id: int,
    ) -> None:
        """Delete an existing education entry."""
        await self.ownership.verify_education(
            education_id,
            user_id,
        )

        education = await self.repository.get_by_id(
            education_id
        )

        if education is None:
            raise HTTPException(
                status_code=404,
                detail="Education not found",
            )

        cv_id = education.cv_id

        await self.repository.delete(
            education
        )

        await self.session.commit()

        await self._invalidate_cv_cache(
            cv_id
        )