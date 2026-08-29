# ==============================
# Library imports
# ==============================

from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import (
    func,
    select,
)


# ==============================
# Application imports
# ==============================

from app.models import (
    CV,
    CVCertification,
    CVEducation,
    CVExperience,
    CVLanguage,
    CVProject,
    CVSkill,
)


# ==============================
# Statistics repository
# ==============================

class StatisticsRepository:
    """
    Provide database operations for CV statistics.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        """
        Initialize the repository with a database session.
        """

        self.session = session

    async def get_user_statistics(
        self,
        user_id: int,
    ) -> dict[str, int]:
        """
        Return aggregated statistics for a user's CVs.
        """

        total_cvs_result = await self.session.execute(
            select(func.count(CV.id))
            .where(
                CV.user_id == user_id
            )
        )

        total_experience_result = await self.session.execute(
            select(func.count(CVExperience.id))
            .join(
                CV,
                CV.id == CVExperience.cv_id,
            )
            .where(
                CV.user_id == user_id
            )
        )

        total_education_result = await self.session.execute(
            select(func.count(CVEducation.id))
            .join(
                CV,
                CV.id == CVEducation.cv_id,
            )
            .where(
                CV.user_id == user_id
            )
        )

        total_projects_result = await self.session.execute(
            select(func.count(CVProject.id))
            .join(
                CV,
                CV.id == CVProject.cv_id,
            )
            .where(
                CV.user_id == user_id
            )
        )

        total_skills_result = await self.session.execute(
            select(func.count(CVSkill.skill_id))
            .join(
                CV,
                CV.id == CVSkill.cv_id,
            )
            .where(
                CV.user_id == user_id
            )
        )

        total_languages_result = await self.session.execute(
            select(func.count(CVLanguage.language_id))
            .join(
                CV,
                CV.id == CVLanguage.cv_id,
            )
            .where(
                CV.user_id == user_id
            )
        )

        total_certifications_result = await self.session.execute(
            select(func.count(CVCertification.id))
            .join(
                CV,
                CV.id == CVCertification.cv_id,
            )
            .where(
                CV.user_id == user_id
            )
        )

        return {
            "total_cvs": total_cvs_result.scalar_one(),
            "total_experience": (
                total_experience_result.scalar_one()
            ),
            "total_education": (
                total_education_result.scalar_one()
            ),
            "total_projects": (
                total_projects_result.scalar_one()
            ),
            "total_skills": (
                total_skills_result.scalar_one()
            ),
            "total_languages": (
                total_languages_result.scalar_one()
            ),
            "total_certifications": (
                total_certifications_result.scalar_one()
            ),
        }