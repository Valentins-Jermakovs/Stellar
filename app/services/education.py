# ==============================
# Library imports
# ==============================

from fastapi import HTTPException

from redis.asyncio import (
    Redis,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)


# ==============================
# Application imports
# ==============================

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


# ==============================
# Service dependencies
# ==============================

from .ownership import CVOwnershipService


# ==============================
# CV education service
# ==============================

class CVEducationService:
    """
    This service handles education entries associated with a CV.

    It provides operations for creating, updating, and deleting
    education entries while verifying CV ownership and maintaining
    the CV detail cache.
    """

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """
        Initialize the CV education service.

        The service uses repositories for database operations,
        an ownership service for authorization, and a cache
        repository for invalidating cached CV details.
        """

        # Database session used by the service.
        self.session = session

        # Repository used to manage education entries.
        self.repository = CVEducationRepository(
            session
        )

        # Service used to verify CV ownership.
        self.ownership = CVOwnershipService(
            session
        )

        # Repository used to manage cached CV data.
        self.cache = CacheRepository(
            redis
        )

    # Build the cache key for a CV detail.
    def _detail_cache_key(
        self,
        cv_id: int,
    ) -> str:
        """
        Build the cache key for a CV detail.
        """

        return f"cv:{cv_id}:detail"

    # Invalidate cached CV details.
    async def _invalidate_cv_cache(
        self,
        cv_id: int,
    ) -> None:
        """
        Remove the cached CV detail.
        """

        await self.cache.delete(
            self._detail_cache_key(
                cv_id
            )
        )

    # Create a new education entry.
    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVEducationCreate,
    ) -> CVEducation:
        """
        Create an education entry for a CV.

        The CV ownership is verified before creating the entry.
        Duplicate education entries are not allowed within the same CV.
        """

        # Verify that the user owns the CV.
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        # Normalize the input data.
        values = DataNormalizer.normalize_model(
            data
        )

        # Check whether the same education entry already exists.
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

        # Create the education model.
        education = CVEducation(
            cv_id=cv_id,
            **values,
        )

        await self.repository.create(
            education
        )

        # Commit and refresh the created entity.
        await self.session.commit()

        await self.session.refresh(
            education
        )

        # Invalidate the cached CV detail.
        await self._invalidate_cv_cache(
            cv_id
        )

        return education

    # Update an existing education entry.
    async def update(
        self,
        education_id: int,
        user_id: int,
        data: CVEducationUpdate,
    ) -> CVEducation:
        """
        Update an existing education entry.

        The entry ownership is verified before applying changes.
        The updated values are also checked against existing
        education entries to prevent duplicates.
        """

        # Verify that the user owns the education entry.
        await self.ownership.verify_education(
            education_id,
            user_id,
        )

        # Retrieve the education entry.
        education = await self.repository.get_by_id(
            education_id
        )

        if education is None:
            raise HTTPException(
                status_code=404,
                detail="Education not found",
            )

        # Normalize only fields provided by the client.
        values = DataNormalizer.normalize_model(
            data,
            exclude_unset=True,
        )

        # Use existing values for fields that were not updated.
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

        # Check for duplicate education entries.
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

        # Apply the updated values.
        for field, value in values.items():
            setattr(
                education,
                field,
                value,
            )

        await self.repository.update(
            education
        )

        # Commit and refresh the updated entity.
        await self.session.commit()

        await self.session.refresh(
            education
        )

        # Invalidate the cached CV detail.
        await self._invalidate_cv_cache(
            education.cv_id
        )

        return education

    # Delete an existing education entry.
    async def delete(
        self,
        education_id: int,
        user_id: int,
    ) -> None:
        """
        Delete an existing education entry.

        The entry ownership is verified before deletion,
        and the related CV cache is invalidated afterwards.
        """

        # Verify that the user owns the education entry.
        await self.ownership.verify_education(
            education_id,
            user_id,
        )

        # Retrieve the education entry.
        education = await self.repository.get_by_id(
            education_id
        )

        if education is None:
            raise HTTPException(
                status_code=404,
                detail="Education not found",
            )

        # Save the CV ID before deleting the entry.
        cv_id = education.cv_id

        await self.repository.delete(
            education
        )

        await self.session.commit()

        # Invalidate the cached CV detail.
        await self._invalidate_cv_cache(
            cv_id
        )