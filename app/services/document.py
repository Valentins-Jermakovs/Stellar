from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import (
    CVCertificationRepository,
    CVEducationRepository,
    CVExperienceRepository,
    CVLanguageRepository,
    CVPersonalInfoRepository,
    CVProjectRepository,
    CVRepository,
    CVSkillRepository,
)

from schemas import (
    CVDocument,
    CVDocumentLanguage,
    CVDocumentSkill,
    CVTemplate,
)


class CVDocumentService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.cv_repository = CVRepository(
            session
        )

        self.personal_info_repository = (
            CVPersonalInfoRepository(
                session
            )
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

        self.skill_repository = (
            CVSkillRepository(
                session
            )
        )

        self.project_repository = (
            CVProjectRepository(
                session
            )
        )

        self.language_repository = (
            CVLanguageRepository(
                session
            )
        )

        self.certification_repository = (
            CVCertificationRepository(
                session
            )
        )

    async def get_document(
        self,
        cv_id: int,
        user_id: int,
    ) -> CVDocument:
        cv = await self.cv_repository.get_by_id_for_user(
            cv_id=cv_id,
            user_id=user_id,
        )

        if cv is None:
            raise HTTPException(
                status_code=404,
                detail="CV not found",
            )

        personal_info = (
            await self.personal_info_repository.get_by_cv_id(
                cv_id
            )
        )

        experience = (
            await self.experience_repository.get_by_cv_id(
                cv_id
            )
        )

        education = (
            await self.education_repository.get_by_cv_id(
                cv_id
            )
        )

        skills = (
            await self.skill_repository.get_with_skills(
                cv_id
            )
        )

        projects = (
            await self.project_repository.get_by_cv_id(
                cv_id
            )
        )

        languages = (
            await self.language_repository.get_with_languages(
                cv_id
            )
        )

        certifications = (
            await self.certification_repository.get_by_cv_id(
                cv_id
            )
        )

        return CVDocument(
            cv_id=cv.id,
            user_id=cv.user_id,
            title=cv.title,
            personal_info=personal_info,
            experience=experience,
            education=education,
            skills=[
                CVDocumentSkill(
                    id=skill.id,
                    name=skill.name,
                    level=cv_skill.level,
                    sort_order=cv_skill.sort_order,
                )
                for cv_skill, skill in skills
            ],
            projects=projects,
            languages=[
                CVDocumentLanguage(
                    id=language.id,
                    name=language.name,
                    proficiency=cv_language.proficiency,
                    sort_order=cv_language.sort_order,
                )
                for cv_language, language in languages
            ],
            certifications=certifications,
        )