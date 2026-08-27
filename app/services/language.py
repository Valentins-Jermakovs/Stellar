from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVLanguage, Language
from app.repositories import (
    CVLanguageRepository,
    LanguageRepository,
)
from app.schemas import (
    CVLanguageCreate,
    CVLanguageUpdate,
    LanguageCreate,
)

from .ownership import CVOwnershipService


class LanguageService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = LanguageRepository(
            session
        )

    async def create(
        self,
        data: LanguageCreate,
    ) -> Language:
        existing = await self.repository.get_by_name(
            data.name
        )

        if existing is not None:
            return existing

        language = Language(
            name=data.name
        )

        return await self.repository.create(
            language
        )

    async def get_by_id(
        self,
        language_id: int,
    ) -> Language:
        language = await self.repository.get_by_id(
            language_id
        )

        if language is None:
            raise HTTPException(
                status_code=404,
                detail="Language not found",
            )

        return language

    async def get_by_name(
        self,
        name: str,
    ) -> Language | None:
        return await self.repository.get_by_name(
            name
        )

    async def get_all(self) -> list[Language]:
        return await self.repository.get_all()


class CVLanguageService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = CVLanguageRepository(
            session
        )

        self.language_repository = LanguageRepository(
            session
        )

        self.ownership = CVOwnershipService(
            session
        )

    async def add(
        self,
        cv_id: int,
        user_id: int,
        data: CVLanguageCreate,
    ) -> CVLanguage:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        language = (
            await self.language_repository.get_by_id(
                data.language_id
            )
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

        cv_language = CVLanguage(
            cv_id=cv_id,
            **data.model_dump(),
        )

        return await self.repository.create(
            cv_language
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> list[CVLanguage]:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        return await self.repository.get_by_cv_id(
            cv_id
        )

    async def update(
        self,
        cv_id: int,
        user_id: int,
        language_id: int,
        data: CVLanguageUpdate,
    ) -> CVLanguage:
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

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(
                cv_language,
                field,
                value,
            )

        return await self.repository.update(
            cv_language
        )

    async def delete(
        self,
        cv_id: int,
        user_id: int,
        language_id: int,
    ) -> None:
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