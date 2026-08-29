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

from app.models import (
    CVLanguage,
    Language,
)

from app.repositories import (
    CacheRepository,
    CVLanguageRepository,
    LanguageRepository,
)

from app.schemas import (
    CVLanguageCreate,
    CVLanguageUpdate,
    LanguageCreate,
)

from app.utils import DataNormalizer


# ==============================
# Service dependencies
# ==============================

from .ownership import CVOwnershipService


# ==============================
# Language service
# ==============================

class LanguageService:
    """
    This service handles the global language catalog.

    It provides operations for creating, retrieving, and searching
    languages that can be associated with CVs.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        """
        Initialize the language service.

        The service uses a language repository to perform
        database operations.
        """

        # Database session used by the service.
        self.session = session

        # Repository used to manage global languages.
        self.repository = LanguageRepository(
            session
        )

    # Create a new global language.
    async def create(
        self,
        data: LanguageCreate,
    ) -> Language:
        """
        Create a language or return an existing one.

        Language names are normalized before checking for an
        existing language.
        """

        # Normalize the input data.
        values = DataNormalizer.normalize_model(
            data
        )

        # Check whether the language already exists.
        existing = await self.repository.get_by_name(
            values["name"]
        )

        if existing is not None:
            return existing

        # Create the language model.
        language = Language(
            name=values["name"]
        )

        await self.repository.create(
            language
        )

        # Commit and refresh the created entity.
        await self.session.commit()

        await self.session.refresh(
            language
        )

        return language

    # Retrieve a global language by ID.
    async def get_by_id(
        self,
        language_id: int,
    ) -> Language:
        """
        Return a global language by ID.

        An HTTP 404 error is raised when the language does not exist.
        """

        # Retrieve the language from the database.
        language = await self.repository.get_by_id(
            language_id
        )

        if language is None:
            raise HTTPException(
                status_code=404,
                detail="Language not found",
            )

        return language

    # Search the global language catalog.
    async def search(
        self,
        query: str | None = None,
    ) -> list[Language]:
        """
        Return up to ten global languages matching the query.
        """

        # Normalize the search query.
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
# CV language service
# ==============================

class CVLanguageService:
    """
    This service handles languages associated with a CV.

    It provides operations for adding, updating, and removing
    languages while verifying CV ownership and maintaining
    the CV detail cache.
    """

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """
        Initialize the CV language service.

        The service uses repositories for database operations,
        an ownership service for authorization, and a cache
        repository for invalidating cached CV details.
        """

        # Database session used by the service.
        self.session = session

        # Repository used to manage CV language associations.
        self.repository = CVLanguageRepository(
            session
        )

        # Repository used to retrieve global languages.
        self.language_repository = LanguageRepository(
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

    # Add a language to a CV.
    async def add(
        self,
        cv_id: int,
        user_id: int,
        data: CVLanguageCreate,
    ) -> CVLanguage:
        """
        Add a global language to a CV.

        The CV ownership and language existence are verified
        before creating the association.
        """

        # Verify that the user owns the CV.
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        # Verify that the global language exists.
        language = await self.language_repository.get_by_id(
            data.language_id
        )

        if language is None:
            raise HTTPException(
                status_code=404,
                detail="Language not found",
            )

        # Check whether the language is already associated with the CV.
        existing = await self.repository.get(
            cv_id,
            data.language_id,
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="Language already added to CV",
            )

        # Normalize the association data.
        values = DataNormalizer.normalize_model(
            data
        )

        # Create the CV language association.
        cv_language = CVLanguage(
            cv_id=cv_id,
            **values,
        )

        await self.repository.create(
            cv_language
        )

        await self.session.commit()

        # Invalidate the cached CV detail.
        await self._invalidate_cv_cache(
            cv_id
        )

        return cv_language

    # Update a CV language association.
    async def update(
        self,
        cv_id: int,
        user_id: int,
        language_id: int,
        data: CVLanguageUpdate,
    ) -> CVLanguage:
        """
        Update a language association in a CV.

        The CV ownership is verified before applying changes.
        """

        # Verify that the user owns the CV.
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        # Retrieve the CV language association.
        cv_language = await self.repository.get(
            cv_id,
            language_id,
        )

        if cv_language is None:
            raise HTTPException(
                status_code=404,
                detail="CV language not found",
            )

        # Normalize only fields provided by the client.
        values = DataNormalizer.normalize_model(
            data,
            exclude_unset=True,
        )

        # Apply the updated values.
        for field, value in values.items():
            setattr(
                cv_language,
                field,
                value,
            )

        await self.repository.update(
            cv_language
        )

        # Commit and refresh the updated entity.
        await self.session.commit()

        await self.session.refresh(
            cv_language
        )

        # Invalidate the cached CV detail.
        await self._invalidate_cv_cache(
            cv_id
        )

        return cv_language

    # Delete a CV language association.
    async def delete(
        self,
        cv_id: int,
        user_id: int,
        language_id: int,
    ) -> None:
        """
        Remove a language association from a CV.

        The CV ownership is verified before deleting the association,
        and the related CV cache is invalidated afterwards.
        """

        # Verify that the user owns the CV.
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        # Retrieve the CV language association.
        cv_language = await self.repository.get(
            cv_id,
            language_id,
        )

        if cv_language is None:
            raise HTTPException(
                status_code=404,
                detail="CV language not found",
            )

        await self.repository.delete(
            cv_language
        )

        await self.session.commit()

        # Invalidate the cached CV detail.
        await self._invalidate_cv_cache(
            cv_id
        )