from sqlalchemy.ext.asyncio import AsyncSession

from models import CVLanguage, Language
from schemas import (
    CVLanguageCreate,
    CVLanguageUpdate,
    LanguageCreate,
)
from services import (
    CVLanguageService,
    LanguageService,
)


class LanguageFacade:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.service = LanguageService(
            session
        )

    async def create(
        self,
        data: LanguageCreate,
    ) -> Language:
        return await self.service.create(
            data
        )

    async def get_by_id(
        self,
        language_id: int,
    ) -> Language:
        return await self.service.get_by_id(
            language_id
        )

    async def get_by_name(
        self,
        name: str,
    ) -> Language | None:
        return await self.service.get_by_name(
            name
        )

    async def get_all(self) -> list[Language]:
        return await self.service.get_all()


class CVLanguageFacade:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.service = CVLanguageService(
            session
        )

    async def add(
        self,
        cv_id: int,
        user_id: int,
        data: CVLanguageCreate,
    ) -> CVLanguage:
        return await self.service.add(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> list[CVLanguage]:
        return await self.service.get_by_cv_id(
            cv_id=cv_id,
            user_id=user_id,
        )

    async def update(
        self,
        cv_id: int,
        user_id: int,
        language_id: int,
        data: CVLanguageUpdate,
    ) -> CVLanguage:
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
        await self.service.delete(
            cv_id=cv_id,
            user_id=user_id,
            language_id=language_id,
        )