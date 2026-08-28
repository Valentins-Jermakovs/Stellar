# Async database session and Redis client used by the services.
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

# Models and schemas used by the facades.
from app.models import CVLanguage, Language
from app.schemas import (
    CVLanguageCreate,
    CVLanguageUpdate,
    LanguageCreate,
)

from app.services import (
    CVLanguageService,
    LanguageService,
)


class LanguageFacade:
    """Provide a simplified interface for the global language catalog."""

    def __init__(
        self,
        session: AsyncSession,
    ):
        """Initialize the facade with service dependencies."""
        self.service = LanguageService(
            session
        )

    async def create(
        self,
        data: LanguageCreate,
    ) -> Language:
        """Create a language or return an existing one."""
        return await self.service.create(
            data
        )

    async def get_by_id(
        self,
        language_id: int,
    ) -> Language:
        """Return a global language by ID."""
        return await self.service.get_by_id(
            language_id
        )

    async def search(
        self,
        query: str | None = None,
    ) -> list[Language]:
        """Search the global language catalog."""
        return await self.service.search(
            query
        )


class CVLanguageFacade:
    """Provide a simplified interface for CV language operations."""

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the facade with service dependencies."""
        self.service = CVLanguageService(
            session=session,
            redis=redis,
        )

    async def add(
        self,
        cv_id: int,
        user_id: int,
        data: CVLanguageCreate,
    ) -> CVLanguage:
        """Add a language to a CV."""
        return await self.service.add(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def update(
        self,
        cv_id: int,
        user_id: int,
        language_id: int,
        data: CVLanguageUpdate,
    ) -> CVLanguage:
        """Update a language association in a CV."""
        return await self.service.update(
            cv_id=cv_id,
            user_id=user_id,
            language_id=language_id,
            data=data,
        )

    async def delete(
        self,
        cv_id: int,
        user_id: int,
        language_id: int,
    ) -> None:
        """Delete a language association from a CV."""
        await self.service.delete(
            cv_id=cv_id,
            user_id=user_id,
            language_id=language_id,
        )