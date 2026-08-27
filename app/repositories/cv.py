from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import (
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
    model = CV

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> list[CV]:
        result = await self.session.execute(
            select(CV)
            .where(CV.user_id == user_id)
            .order_by(CV.updated_at.desc())
        )

        return list(result.scalars().all())

    async def get_by_id_for_user(
        self,
        cv_id: int,
        user_id: int,
    ) -> CV | None:
        result = await self.session.execute(
            select(CV).where(
                CV.id == cv_id,
                CV.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()


class CVPersonalInfoRepository(
    BaseRepository[CVPersonalInfo]
):
    model = CVPersonalInfo

    async def get_by_cv_id(
        self,
        cv_id: int,
    ) -> CVPersonalInfo | None:
        result = await self.session.execute(
            select(CVPersonalInfo).where(
                CVPersonalInfo.cv_id == cv_id
            )
        )

        return result.scalar_one_or_none()


class CVExperienceRepository(
    BaseRepository[CVExperience]
):
    model = CVExperience

    async def get_by_cv_id(
        self,
        cv_id: int,
    ) -> list[CVExperience]:
        result = await self.session.execute(
            select(CVExperience)
            .where(CVExperience.cv_id == cv_id)
            .order_by(CVExperience.sort_order)
        )

        return list(result.scalars().all())


class CVEducationRepository(
    BaseRepository[CVEducation]
):
    model = CVEducation

    async def get_by_cv_id(
        self,
        cv_id: int,
    ) -> list[CVEducation]:
        result = await self.session.execute(
            select(CVEducation)
            .where(CVEducation.cv_id == cv_id)
            .order_by(CVEducation.sort_order)
        )

        return list(result.scalars().all())


class SkillRepository(BaseRepository[Skill]):
    model = Skill

    async def get_by_name(
        self,
        name: str,
    ) -> Skill | None:
        result = await self.session.execute(
            select(Skill).where(
                Skill.name == name
            )
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[Skill]:
        result = await self.session.execute(
            select(Skill).order_by(Skill.name)
        )

        return list(result.scalars().all())


class CVSkillRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create(
        self,
        cv_skill: CVSkill,
    ) -> CVSkill:
        self.session.add(cv_skill)
        await self.session.flush()

        return cv_skill

    async def get(
        self,
        cv_id: int,
        skill_id: int,
    ) -> CVSkill | None:
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
        result = await self.session.execute(
            select(CVSkill)
            .where(CVSkill.cv_id == cv_id)
            .order_by(CVSkill.sort_order)
        )

        return list(result.scalars().all())

    async def get_with_skills(
        self,
        cv_id: int,
    ) -> list[tuple[CVSkill, Skill]]:
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

        return list(result.all())

    async def update(
        self,
        cv_skill: CVSkill,
    ) -> CVSkill:
        await self.session.flush()

        return cv_skill

    async def delete(
        self,
        cv_skill: CVSkill,
    ) -> None:
        await self.session.delete(cv_skill)
        await self.session.flush()


class CVProjectRepository(
    BaseRepository[CVProject]
):
    model = CVProject

    async def get_by_cv_id(
        self,
        cv_id: int,
    ) -> list[CVProject]:
        result = await self.session.execute(
            select(CVProject)
            .where(CVProject.cv_id == cv_id)
            .order_by(CVProject.sort_order)
        )

        return list(result.scalars().all())


class LanguageRepository(
    BaseRepository[Language]
):
    model = Language

    async def get_by_name(
        self,
        name: str,
    ) -> Language | None:
        result = await self.session.execute(
            select(Language).where(
                Language.name == name
            )
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[Language]:
        result = await self.session.execute(
            select(Language).order_by(Language.name)
        )

        return list(result.scalars().all())


class CVLanguageRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create(
        self,
        cv_language: CVLanguage,
    ) -> CVLanguage:
        self.session.add(cv_language)
        await self.session.flush()

        return cv_language

    async def get(
        self,
        cv_id: int,
        language_id: int,
    ) -> CVLanguage | None:
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
        result = await self.session.execute(
            select(CVLanguage)
            .where(CVLanguage.cv_id == cv_id)
            .order_by(CVLanguage.sort_order)
        )

        return list(result.scalars().all())

    async def get_with_languages(
        self,
        cv_id: int,
    ) -> list[tuple[CVLanguage, Language]]:
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

        return list(result.all())

    async def update(
        self,
        cv_language: CVLanguage,
    ) -> CVLanguage:
        await self.session.flush()

        return cv_language

    async def delete(
        self,
        cv_language: CVLanguage,
    ) -> None:
        await self.session.delete(cv_language)
        await self.session.flush()


class CVCertificationRepository(
    BaseRepository[CVCertification]
):
    model = CVCertification

    async def get_by_cv_id(
        self,
        cv_id: int,
    ) -> list[CVCertification]:
        result = await self.session.execute(
            select(CVCertification)
            .where(CVCertification.cv_id == cv_id)
            .order_by(CVCertification.sort_order)
        )

        return list(result.scalars().all())