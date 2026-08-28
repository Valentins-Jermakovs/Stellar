from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVPersonalInfo
from app.repositories import CVPersonalInfoRepository
from app.schemas import (
    CVPersonalInfoCreate,
    CVPersonalInfoUpdate,
)
from app.utils import DataNormalizer

from .ownership import CVOwnershipService


class CVPersonalInfoService:
    """Handle personal information associated with a CV."""

    def __init__(
        self,
        session: AsyncSession,
    ):
        """Initialize the service dependencies."""
        self.session = session

        self.repository = CVPersonalInfoRepository(
            session
        )

        self.ownership = CVOwnershipService(
            session
        )

    async def create(
        self,
        cv_id: int,
        user_id: int,
        data: CVPersonalInfoCreate,
    ) -> CVPersonalInfo:
        """Create personal information for a CV."""
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        # Each CV can have only one personal information record.
        existing = await self.repository.get_by_cv_id(
            cv_id
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="Personal information already exists",
            )

        values = DataNormalizer.normalize_model(
            data
        )

        personal_info = CVPersonalInfo(
            cv_id=cv_id,
            **values,
        )

        await self.repository.create(
            personal_info
        )

        await self.session.commit()
        await self.session.refresh(
            personal_info
        )

        return personal_info

    async def update(
        self,
        cv_id: int,
        user_id: int,
        data: CVPersonalInfoUpdate,
    ) -> CVPersonalInfo:
        """Update personal information for a CV."""
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        personal_info = (
            await self.repository.get_by_cv_id(
                cv_id
            )
        )

        if personal_info is None:
            raise HTTPException(
                status_code=404,
                detail="Personal information not found",
            )

        # Keep only fields provided by the client and normalize strings.
        values = DataNormalizer.normalize_model(
            data,
            exclude_unset=True,
        )

        for field, value in values.items():
            setattr(
                personal_info,
                field,
                value,
            )

        await self.repository.update(
            personal_info
        )

        await self.session.commit()
        await self.session.refresh(
            personal_info
        )

        return personal_info

    async def delete(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        """Delete personal information from a CV."""
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        personal_info = (
            await self.repository.get_by_cv_id(
                cv_id
            )
        )

        if personal_info is None:
            raise HTTPException(
                status_code=404,
                detail="Personal information not found",
            )

        await self.repository.delete(
            personal_info
        )

        await self.session.commit()