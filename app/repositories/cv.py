# AsyncSession is used by repositories to execute database queries.
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

# SQL query helpers used to select records and calculate totals.
from sqlmodel import func, select

from app.models import (
    CV,
    CVCertification,
    CVEducation,
    CVExperience,
    CVLanguage,
    CVPersonalInfo,
    CVProject,
    CVSkill,
    Language,
    Skill,
)

from .base import BaseRepository


class CVRepository(BaseRepository[CV]):
    """Repository for CV database operations."""

    model = CV

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> list[CV]:
        """Return all CVs belonging to a user."""
        result = await self.session.execute(
            select(CV)
            .where(
                CV.user_id == user_id
            )
            .order_by(
                CV.updated_at.desc()
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_by_title(
        self,
        title: str,
    ) -> CV | None:
        """Return a CV by title, if it exists."""
        result = await self.session.execute(
            select(CV).where(
                CV.title == title
            )
        )

        return result.scalar_one_or_none()

    async def get_by_id_for_user(
        self,
        cv_id: int,
        user_id: int,
    ) -> CV | None:
        """Return a user's CV by ID."""
        result = await self.session.execute(
            select(CV).where(
                CV.id == cv_id,
                CV.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def search_by_user(
        self,
        user_id: int,
        query: str | None,
        offset: int,
        limit: int,
    ) -> tuple[list[CV], int]:
        """Search a user's CVs and return the results with total count."""
        filters = [
            CV.user_id == user_id,
        ]

        if query:
            filters.append(
                CV.title.ilike(
                    f"%{query}%"
                )
            )

        total_result = await self.session.execute(
            select(func.count())
            .select_from(CV)
            .where(*filters)
        )

        total = total_result.scalar_one()

        result = await self.session.execute(
            select(CV)
            .where(*filters)
            .order_by(
                CV.updated_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        cvs = list(
            result.scalars().all()
        )

        return cvs, total


class CVPersonalInfoRepository(
    BaseRepository[CVPersonalInfo]
):
    """Repository for CV personal information."""

    model = CVPersonalInfo

    async def get_by_cv_id(
        self,
        cv_id: int,
    ) -> CVPersonalInfo | None:
        """Return personal information for a CV."""
        result = await self.session.execute(
            select(CVPersonalInfo).where(
                CVPersonalInfo.cv_id == cv_id
            )
        )

        return result.scalar_one_or_none()


class CVExperienceRepository(
    BaseRepository[CVExperience]
):
    """Repository for CV experience entries."""

    model = CVExperience

    async def get_by_cv_id(
        self,
        cv_id: int,
    ) -> list[CVExperience]:
        """Return all experience entries for a CV."""
        result = await self.session.execute(
            select(CVExperience)
            .where(
                CVExperience.cv_id == cv_id
            )
            .order_by(
                CVExperience.sort_order
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_duplicate(
        self,
        cv_id: int,
        company: str,
        position: str,
        start_date: date,
        exclude_id: int | None = None,
    ) -> CVExperience | None:
        """Return a duplicate experience entry, if one exists."""
        filters = [
            CVExperience.cv_id == cv_id,
            CVExperience.company == company,
            CVExperience.position == position,
            CVExperience.start_date == start_date,
        ]

        if exclude_id is not None:
            filters.append(
                CVExperience.id != exclude_id
            )

        result = await self.session.execute(
            select(CVExperience)
            .where(*filters)
        )

        return result.scalar_one_or_none()


class CVEducationRepository(
    BaseRepository[CVEducation]
):
    """Repository for CV education entries."""

    model = CVEducation

    async def get_by_cv_id(
        self,
        cv_id: int,
    ) -> list[CVEducation]:
        """Return all education entries for a CV."""
        result = await self.session.execute(
            select(CVEducation)
            .where(
                CVEducation.cv_id == cv_id
            )
            .order_by(
                CVEducation.sort_order
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_duplicate(
        self,
        cv_id: int,
        institution: str,
        degree: str | None,
        field_of_study: str | None,
        start_date: date | None,
        exclude_id: int | None = None,
    ) -> CVEducation | None:
        """Return a duplicate education entry, if one exists."""
        filters = [
            CVEducation.cv_id == cv_id,
            CVEducation.institution == institution,
            CVEducation.degree == degree,
            CVEducation.field_of_study == field_of_study,
            CVEducation.start_date == start_date,
        ]

        if exclude_id is not None:
            filters.append(
                CVEducation.id != exclude_id
            )

        result = await self.session.execute(
            select(CVEducation)
            .where(*filters)
        )

        return result.scalar_one_or_none()


class SkillRepository(BaseRepository[Skill]):
    """Repository for reusable skills."""

    model = Skill

    async def get_by_name(
        self,
        name: str,
    ) -> Skill | None:
        """Return a skill by name."""
        result = await self.session.execute(
            select(Skill).where(
                Skill.name == name
            )
        )

        return result.scalar_one_or_none()

    async def search(
        self,
        query: str | None = None,
        limit: int = 10,
    ) -> list[Skill]:
        """Return up to ten skills matching the search query."""
        filters = []

        if query:
            filters.append(
                Skill.name.ilike(
                    f"%{query}%"
                )
            )

        result = await self.session.execute(
            select(Skill)
            .where(*filters)
            .order_by(
                Skill.name
            )
            .limit(limit)
        )

        return list(
            result.scalars().all()
        )


class CVSkillRepository:
    """Repository for CV-to-skill associations."""

    def __init__(
        self,
        session: AsyncSession,
    ):
        """Initialize the repository with a database session."""
        self.session = session

    async def create(
        self,
        cv_skill: CVSkill,
    ) -> CVSkill:
        """Create a CV-to-skill association."""
        self.session.add(cv_skill)
        await self.session.flush()

        return cv_skill

    async def get(
        self,
        cv_id: int,
        skill_id: int,
    ) -> CVSkill | None:
        """Return a CV-to-skill association."""
        result = await self.session.execute(
            select(CVSkill).where(
                CVSkill.cv_id == cv_id,
                CVSkill.skill_id == skill_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_cv_id(
        self,
        cv_id: int,
    ) -> list[CVSkill]:
        """Return all skill associations for a CV."""
        result = await self.session.execute(
            select(CVSkill)
            .where(
                CVSkill.cv_id == cv_id
            )
            .order_by(
                CVSkill.sort_order
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_with_skills(
        self,
        cv_id: int,
    ) -> list[tuple[CVSkill, Skill]]:
        """Return skill associations together with their skills."""
        result = await self.session.execute(
            select(
                CVSkill,
                Skill,
            )
            .join(
                Skill,
                Skill.id == CVSkill.skill_id,
            )
            .where(
                CVSkill.cv_id == cv_id
            )
            .order_by(
                CVSkill.sort_order
            )
        )

        return list(
            result.all()
        )

    async def update(
        self,
        cv_skill: CVSkill,
    ) -> CVSkill:
        """Flush changes to a CV-to-skill association."""
        await self.session.flush()

        return cv_skill

    async def delete(
        self,
        cv_skill: CVSkill,
    ) -> None:
        """Delete a CV-to-skill association."""
        await self.session.delete(cv_skill)
        await self.session.flush()


class CVProjectRepository(
    BaseRepository[CVProject]
):
    """Repository for CV project entries."""

    model = CVProject

    async def get_by_cv_id(
        self,
        cv_id: int,
    ) -> list[CVProject]:
        """Return all projects associated with a CV."""
        result = await self.session.execute(
            select(CVProject)
            .where(
                CVProject.cv_id == cv_id
            )
            .order_by(
                CVProject.sort_order
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_duplicate(
        self,
        cv_id: int,
        name: str,
        exclude_id: int | None = None,
    ) -> CVProject | None:
        """Return a duplicate project in a CV, if one exists."""
        filters = [
            CVProject.cv_id == cv_id,
            CVProject.name == name,
        ]

        if exclude_id is not None:
            filters.append(
                CVProject.id != exclude_id
            )

        result = await self.session.execute(
            select(CVProject)
            .where(*filters)
        )

        return result.scalar_one_or_none()


class LanguageRepository(
    BaseRepository[Language]
):
    """Repository for reusable languages."""

    model = Language

    async def get_by_name(
        self,
        name: str,
    ) -> Language | None:
        """Return a language by name."""
        result = await self.session.execute(
            select(Language).where(
                Language.name == name
            )
        )

        return result.scalar_one_or_none()

    async def search(
        self,
        query: str | None = None,
        limit: int = 10,
    ) -> list[Language]:
        """Return up to ten languages matching the search query."""
        filters = []

        if query:
            filters.append(
                Language.name.ilike(
                    f"%{query}%"
                )
            )

        result = await self.session.execute(
            select(Language)
            .where(*filters)
            .order_by(
                Language.name
            )
            .limit(limit)
        )

        return list(
            result.scalars().all()
        )


class CVLanguageRepository:
    """Repository for CV-to-language associations."""

    def __init__(
        self,
        session: AsyncSession,
    ):
        """Initialize the repository with a database session."""
        self.session = session

    async def create(
        self,
        cv_language: CVLanguage,
    ) -> CVLanguage:
        """Create a CV-to-language association."""
        self.session.add(cv_language)
        await self.session.flush()

        return cv_language

    async def get(
        self,
        cv_id: int,
        language_id: int,
    ) -> CVLanguage | None:
        """Return a CV-to-language association."""
        result = await self.session.execute(
            select(CVLanguage).where(
                CVLanguage.cv_id == cv_id,
                CVLanguage.language_id == language_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_cv_id(
        self,
        cv_id: int,
    ) -> list[CVLanguage]:
        """Return all language associations for a CV."""
        result = await self.session.execute(
            select(CVLanguage)
            .where(
                CVLanguage.cv_id == cv_id
            )
            .order_by(
                CVLanguage.sort_order
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_with_languages(
        self,
        cv_id: int,
    ) -> list[tuple[CVLanguage, Language]]:
        """Return language associations together with their languages."""
        result = await self.session.execute(
            select(
                CVLanguage,
                Language,
            )
            .join(
                Language,
                Language.id == CVLanguage.language_id,
            )
            .where(
                CVLanguage.cv_id == cv_id
            )
            .order_by(
                CVLanguage.sort_order
            )
        )

        return list(
            result.all()
        )

    async def update(
        self,
        cv_language: CVLanguage,
    ) -> CVLanguage:
        """Flush changes to a CV-to-language association."""
        await self.session.flush()

        return cv_language

    async def delete(
        self,
        cv_language: CVLanguage,
    ) -> None:
        """Delete a CV-to-language association."""
        await self.session.delete(cv_language)
        await self.session.flush()


class CVCertificationRepository(
    BaseRepository[CVCertification]
):
    """Repository for CV certification entries."""

    model = CVCertification

    async def get_by_cv_id(
        self,
        cv_id: int,
    ) -> list[CVCertification]:
        """Return all certifications associated with a CV."""
        result = await self.session.execute(
            select(CVCertification)
            .where(
                CVCertification.cv_id == cv_id
            )
            .order_by(
                CVCertification.sort_order
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_duplicate(
        self,
        cv_id: int,
        name: str,
        exclude_id: int | None = None,
    ) -> CVCertification | None:
        """Return a duplicate certification in a CV, if one exists."""
        filters = [
            CVCertification.cv_id == cv_id,
            CVCertification.name == name,
        ]

        # Ignore the current certification when checking during an update.
        if exclude_id is not None:
            filters.append(
                CVCertification.id != exclude_id
            )

        result = await self.session.execute(
            select(CVCertification)
            .where(*filters)
        )

        return result.scalar_one_or_none()