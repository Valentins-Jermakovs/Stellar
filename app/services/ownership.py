# ==============================
# Library imports
# ==============================

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


# ==============================
# Repository imports
# ==============================

from app.repositories import (
    CVCertificationRepository,
    CVEducationRepository,
    CVExperienceRepository,
    CVProjectRepository,
    CVRepository,
)


# ==============================
# CV ownership service
# ==============================

class CVOwnershipService:
    """
    This class handles ownership verification for CVs
    and their related entities.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        """
        Initialize the service dependencies.
        """

        self.cv_repository = CVRepository(
            session
        )

        self.experience_repository = (
            CVExperienceRepository(
                session
            )
        )

        self.education_repository = (
            CVEducationRepository(
                session
            )
        )

        self.project_repository = (
            CVProjectRepository(
                session
            )
        )

        self.certification_repository = (
            CVCertificationRepository(
                session
            )
        )

    # Verify CV ownership.
    async def verify_cv(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        """
        Verify that a CV belongs to the current user.
        """

        cv = await self.cv_repository.get_by_id_for_user(
            cv_id=cv_id,
            user_id=user_id,
        )

        if cv is None:
            raise HTTPException(
                status_code=404,
                detail="CV not found",
            )

    # Verify work experience ownership.
    async def verify_experience(
        self,
        experience_id: int,
        user_id: int,
    ) -> None:
        """
        Verify that a work experience entry belongs to the current user.
        """

        experience = (
            await self.experience_repository.get_by_id(
                experience_id
            )
        )

        if experience is None:
            raise HTTPException(
                status_code=404,
                detail="Experience not found",
            )

        await self.verify_cv(
            cv_id=experience.cv_id,
            user_id=user_id,
        )

    # Verify education ownership.
    async def verify_education(
        self,
        education_id: int,
        user_id: int,
    ) -> None:
        """
        Verify that an education entry belongs to the current user.
        """

        education = (
            await self.education_repository.get_by_id(
                education_id
            )
        )

        if education is None:
            raise HTTPException(
                status_code=404,
                detail="Education not found",
            )

        await self.verify_cv(
            cv_id=education.cv_id,
            user_id=user_id,
        )

    # Verify project ownership.
    async def verify_project(
        self,
        project_id: int,
        user_id: int,
    ) -> None:
        """
        Verify that a project belongs to the current user.
        """

        project = (
            await self.project_repository.get_by_id(
                project_id
            )
        )

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found",
            )

        await self.verify_cv(
            cv_id=project.cv_id,
            user_id=user_id,
        )

    # Verify certification ownership.
    async def verify_certification(
        self,
        certification_id: int,
        user_id: int,
    ) -> None:
        """
        Verify that a certification belongs to the current user.
        """

        certification = (
            await self.certification_repository.get_by_id(
                certification_id
            )
        )

        if certification is None:
            raise HTTPException(
                status_code=404,
                detail="Certification not found",
            )

        await self.verify_cv(
            cv_id=certification.cv_id,
            user_id=user_id,
        )

    # Verify personal information ownership.
    async def verify_personal_info(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        """
        Verify ownership of the CV personal information.
        """

        await self.verify_cv(
            cv_id=cv_id,
            user_id=user_id,
        )

    # Verify CV skill ownership.
    async def verify_skill(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        """
        Verify ownership of a CV skill.
        """

        await self.verify_cv(
            cv_id=cv_id,
            user_id=user_id,
        )

    # Verify CV language ownership.
    async def verify_language(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        """
        Verify ownership of a CV language.
        """

        await self.verify_cv(
            cv_id=cv_id,
            user_id=user_id,
        )