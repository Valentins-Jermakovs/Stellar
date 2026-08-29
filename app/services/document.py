# ==============================
# Library imports
# ==============================

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)


# ==============================
# Application imports
# ==============================

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

from app.schemas import (
    CVDocument,
    CVDocumentLanguage,
    CVDocumentSkill,
    CVTemplate,
)


# ==============================
# CV document service
# ==============================

class CVDocumentService:
    """
    This service builds a complete CV document.

    It collects the CV data and all related entities from the database
    and prepares a single document that can be passed to the CV generator.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        """
        Initialize the CV document service.

        The service creates repositories used to retrieve the CV
        and all of its related data.
        """

        # Repository used to retrieve the CV.
        self.cv_repository = CVRepository(
            session
        )

        # Repository used to retrieve personal information.
        self.personal_info_repository = (
            CVPersonalInfoRepository(
                session
            )
        )

        # Repository used to retrieve work experience.
        self.experience_repository = (
            CVExperienceRepository(
                session
            )
        )

        # Repository used to retrieve education.
        self.education_repository = (
            CVEducationRepository(
                session
            )
        )

        # Repository used to retrieve CV skills.
        self.skill_repository = (
            CVSkillRepository(
                session
            )
        )

        # Repository used to retrieve projects.
        self.project_repository = (
            CVProjectRepository(
                session
            )
        )

        # Repository used to retrieve CV languages.
        self.language_repository = (
            CVLanguageRepository(
                session
            )
        )

        # Repository used to retrieve certifications.
        self.certification_repository = (
            CVCertificationRepository(
                session
            )
        )

    async def get_document(
        self,
        cv_id: int,
        user_id: int,
        template: CVTemplate,
    ) -> CVDocument:
        """
        Build a complete CV document.

        The CV must belong to the authenticated user.
        All related CV data is retrieved and combined into a
        single document according to the selected template.
        """

        # Retrieve the CV and verify ownership.
        cv = await self.cv_repository.get_by_id_for_user(
            cv_id=cv_id,
            user_id=user_id,
        )

        if cv is None:
            raise HTTPException(
                status_code=404,
                detail="CV not found",
            )

        # Retrieve personal information.
        personal_info = (
            await self.personal_info_repository.get_by_cv_id(
                cv_id
            )
        )

        # Retrieve work experience.
        experience = (
            await self.experience_repository.get_by_cv_id(
                cv_id
            )
        )

        # Retrieve education.
        education = (
            await self.education_repository.get_by_cv_id(
                cv_id
            )
        )

        # Retrieve skills together with their global definitions.
        skills = (
            await self.skill_repository.get_with_skills(
                cv_id
            )
        )

        # Retrieve projects.
        projects = (
            await self.project_repository.get_by_cv_id(
                cv_id
            )
        )

        # Retrieve languages together with their global definitions.
        languages = (
            await self.language_repository.get_with_languages(
                cv_id
            )
        )

        # Retrieve certifications.
        certifications = (
            await self.certification_repository.get_by_cv_id(
                cv_id
            )
        )

        # Build and return the complete CV document.
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
            template=template,
        )