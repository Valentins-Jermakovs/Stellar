from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVLanguage, Language
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

from .ownership import CVOwnershipService


class LanguageService:
    """Handle the global language catalog."""

    def __init__(
        self,
        session: AsyncSession,
    ):
        """Initialize the service dependencies."""
        self.session = session

        self.repository = LanguageRepository(
            session
        )

    async def create(
        self,
        data: LanguageCreate,
    ) -> Language:
        """Create a language or return an existing one."""
        values = DataNormalizer.normalize_model(
            data
        )

        existing = await self.repository.get_by_name(
            values["name"]
        )

        if existing is not None:
            return existing

        language = Language(
            name=values["name"]
        )

        await self.repository.create(
            language
        )

        await self.session.commit()
        await self.session.refresh(
            language
        )

        return language

    async def get_by_id(
        self,
        language_id: int,
    ) -> Language:
        """Return a global language by ID."""
        language = await self.repository.get_by_id(
            language_id
        )

        if language is None:
            raise HTTPException(
                status_code=404,
                detail="Language not found",
            )

        return language

    async def search(
        self,
        query: str | None = None,
    ) -> list[Language]:
        """Return up to ten global languages matching the query."""
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


class CVLanguageService:
    """Handle languages associated with a CV."""

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the service dependencies."""
        self.session = session

        self.repository = CVLanguageRepository(
            session
        )

        self.language_repository = LanguageRepository(
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

    async def add(
        self,
        cv_id: int,
        user_id: int,
        data: CVLanguageCreate,
    ) -> CVLanguage:
        """Add a global language to a CV."""
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        language = await self.language_repository.get_by_id(
            data.language_id
        )

        if language is None:
            raise HTTPException(
                status_code=404,
                detail="Language not found",
            )

        existing = await self.repository.get(
            cv_id,
            data.language_id,
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="Language already added to CV",
            )

        values = DataNormalizer.normalize_model(
            data
        )

        cv_language = CVLanguage(
            cv_id=cv_id,
            **values,
        )

        await self.repository.create(
            cv_language
        )

        await self.session.commit()

        await self._invalidate_cv_cache(
            cv_id
        )

        return cv_language

    async def update(
        self,
        cv_id: int,
        user_id: int,
        language_id: int,
        data: CVLanguageUpdate,
    ) -> CVLanguage:
        """Update a language association in a CV."""
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        cv_language = await self.repository.get(
            cv_id,
            language_id,
        )

        if cv_language is None:
            raise HTTPException(
                status_code=404,
                detail="CV language not found",
            )

        values = DataNormalizer.normalize_model(
            data,
            exclude_unset=True,
        )

        for field, value in values.items():
            setattr(
                cv_language,
                field,
                value,
            )

        await self.repository.update(
            cv_language
        )

        await self.session.commit()
        await self.session.refresh(
            cv_language
        )

        await self._invalidate_cv_cache(
            cv_id
        )

        return cv_language

    async def delete(
        self,
        cv_id: int,
        user_id: int,
        language_id: int,
    ) -> None:
        """Remove a language association from a CV."""
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

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

        await self._invalidate_cv_cache(
            cv_id
        )