from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVSkill, Skill
from app.repositories import (
    CVSkillRepository,
    SkillRepository,
)
from app.schemas import (
    CVSkillCreate,
    CVSkillUpdate,
    SkillCreate,
)

from .ownership import CVOwnershipService


class SkillService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = SkillRepository(session)

    async def create(
        self,
        data: SkillCreate,
    ) -> Skill:
        existing = await self.repository.get_by_name(
            data.name
        )

        if existing is not None:
            return existing

        skill = Skill(
            name=data.name
        )

        return await self.repository.create(skill)

    async def get_by_id(
        self,
        skill_id: int,
    ) -> Skill:
        skill = await self.repository.get_by_id(
            skill_id
        )

        if skill is None:
            raise HTTPException(
                status_code=404,
                detail="Skill not found",
            )

        return skill

    async def get_all(self) -> list[Skill]:
        return await self.repository.get_all()

    async def get_by_name(
        self,
        name: str,
    ) -> Skill | None:
        return await self.repository.get_by_name(
            name
        )


class CVSkillService:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repository = CVSkillRepository(
            session
        )

        self.skill_repository = SkillRepository(
            session
        )

        self.ownership = CVOwnershipService(
            session
        )

    async def add(
        self,
        cv_id: int,
        user_id: int,
        data: CVSkillCreate,
    ) -> CVSkill:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        skill = await self.skill_repository.get_by_id(
            data.skill_id
        )

        if skill is None:
            raise HTTPException(
                status_code=404,
                detail="Skill not found",
            )

        existing = await self.repository.get(
            cv_id,
            data.skill_id,
        )

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="Skill already added to CV",
            )

        cv_skill = CVSkill(
            cv_id=cv_id,
            **data.model_dump(),
        )

        return await self.repository.create(
            cv_skill
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> list[CVSkill]:
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
        skill_id: int,
        data: CVSkillUpdate,
    ) -> CVSkill:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        cv_skill = await self.repository.get(
            cv_id,
            skill_id,
        )

        if cv_skill is None:
            raise HTTPException(
                status_code=404,
                detail="CV skill not found",
            )

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(
                cv_skill,
                field,
                value,
            )

        return await self.repository.update(
            cv_skill
        )

    async def delete(
        self,
        cv_id: int,
        user_id: int,
        skill_id: int,
    ) -> None:
        await self.ownership.verify_cv(
            cv_id,
            user_id,
        )

        cv_skill = await self.repository.get(
            cv_id,
            skill_id,
        )

        if cv_skill is None:
            raise HTTPException(
                status_code=404,
                detail="CV skill not found",
            )

        await self.repository.delete(
            cv_skill
        )