from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVCertification
from app.repositories import (
    CacheRepository,
    CVCertificationRepository,
)
from app.schemas import (
    CVCertificationCreate,
    CVCertificationUpdate,
)
from app.utils import DataNormalizer

from .ownership import CVOwnershipService


class CVCertificationService:
    """Handle certifications associated with a CV."""

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the service dependencies."""
        self.session = session

        self.repository = CVCertificationRepository(
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
        data: CVCertificationCreate,
    ) -> CVCertification:
        """Create a certification for a CV."""
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
                detail="This certification already exists",
            )

        certification = CVCertification(
            cv_id=cv_id,
            **values,
        )

        await self.repository.create(
            certification
        )

        await self.session.commit()
        await self.session.refresh(
            certification
        )

        await self._invalidate_cv_cache(
            cv_id
        )

        return certification

    async def update(
        self,
        certification_id: int,
        user_id: int,
        data: CVCertificationUpdate,
    ) -> CVCertification:
        """Update an existing certification."""
        certification = await self.repository.get_by_id(
            certification_id
        )

        if certification is None:
            raise HTTPException(
                status_code=404,
                detail="Certification not found",
            )

        await self.ownership.verify_certification(
            certification_id,
            user_id,
        )

        values = DataNormalizer.normalize_model(
            data,
            exclude_unset=True,
        )

        name = values.get(
            "name",
            certification.name,
        )

        existing = await self.repository.get_duplicate(
            cv_id=certification.cv_id,
            name=name,
            exclude_id=certification_id,
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="This certification already exists",
            )

        for field, value in values.items():
            setattr(
                certification,
                field,
                value,
            )

        await self.repository.update(
            certification
        )

        await self.session.commit()
        await self.session.refresh(
            certification
        )

        await self._invalidate_cv_cache(
            certification.cv_id
        )

        return certification

    async def delete(
        self,
        certification_id: int,
        user_id: int,
    ) -> None:
        """Delete an existing certification."""
        certification = await self.repository.get_by_id(
            certification_id
        )

        if certification is None:
            raise HTTPException(
                status_code=404,
                detail="Certification not found",
            )

        await self.ownership.verify_certification(
            certification_id,
            user_id,
        )

        cv_id = certification.cv_id

        await self.repository.delete(
            certification
        )

        await self.session.commit()

        await self._invalidate_cv_cache(
            cv_id
        )

