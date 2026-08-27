from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import (
    CVCertificationRepository,
    CVEducationRepository,
    CVExperienceRepository,
    CVLanguageRepository,
    CVPersonalInfoRepository,
    CVProjectRepository,
    CVRepository,
    CVSkillRepository,
)


class CVOwnershipService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.cv_repository = CVRepository(session)

        self.personal_info_repository = (
            CVPersonalInfoRepository(session)
        )

        self.experience_repository = (
            CVExperienceRepository(session)
        )

        self.education_repository = (
            CVEducationRepository(session)
        )

        self.skill_repository = (
            CVSkillRepository(session)
        )

        self.project_repository = (
            CVProjectRepository(session)
        )

        self.language_repository = (
            CVLanguageRepository(session)
        )

        self.certification_repository = (
            CVCertificationRepository(session)
        )

    async def verify_cv(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        cv = await self.cv_repository.get_by_id(
            cv_id
        )

        if cv is None or cv.user_id != user_id:
            raise HTTPException(
                status_code=404,
                detail="CV not found",
            )

    async def verify_experience(
        self,
        experience_id: int,
        user_id: int,
    ) -> None:
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
            experience.cv_id,
            user_id,
        )

    async def verify_education(
        self,
        education_id: int,
        user_id: int,
    ) -> None:
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
            education.cv_id,
            user_id,
        )

    async def verify_project(
        self,
        project_id: int,
        user_id: int,
    ) -> None:
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
            project.cv_id,
            user_id,
        )

    async def verify_certification(
        self,
        certification_id: int,
        user_id: int,
    ) -> None:
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
            certification.cv_id,
            user_id,
        )

    async def verify_personal_info(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        await self.verify_cv(
            cv_id,
            user_id,
        )

    async def verify_skill(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        await self.verify_cv(
            cv_id,
            user_id,
        )

    async def verify_language(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        await self.verify_cv(
            cv_id,
            user_id,
        )