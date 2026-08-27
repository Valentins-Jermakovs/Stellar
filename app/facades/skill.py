from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CVSkill, Skill
from app.schemas import (
    CVSkillCreate,
    CVSkillUpdate,
    SkillCreate,
)
from app.services import (
    CVSkillService,
    SkillService,
)


class SkillFacade:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.service = SkillService(
            session
        )

    async def create(
        self,
        data: SkillCreate,
    ) -> Skill:
        return await self.service.create(
            data
        )

    async def get_by_id(
        self,
        skill_id: int,
    ) -> Skill:
        return await self.service.get_by_id(
            skill_id
        )

    async def get_all(self) -> list[Skill]:
        return await self.service.get_all()

    async def get_by_name(
        self,
        name: str,
    ) -> Skill | None:
        return await self.service.get_by_name(
            name
        )


class CVSkillFacade:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.service = CVSkillService(
            session
        )

    async def add(
        self,
        cv_id: int,
        user_id: int,
        data: CVSkillCreate,
    ) -> CVSkill:
        return await self.service.add(
            cv_id=cv_id,
            user_id=user_id,
            data=data,
        )

    async def get_by_cv_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> list[CVSkill]:
        return await self.service.get_by_cv_id(
            cv_id=cv_id,
            user_id=user_id,
        )

    async def update(
        self,
        cv_id: int,
        user_id: int,
        skill_id: int,
        data: CVSkillUpdate,
    ) -> CVSkill:
        return await self.service.update(
            cv_id=cv_id,
            user_id=user_id,
            skill_id=skill_id,
            data=data,
        )

    async def delete(
        self,
        cv_id: int,
        user_id: int,
        skill_id: int,
    ) -> None:
        await self.service.delete(
            cv_id=cv_id,
            user_id=user_id,
            skill_id=skill_id,
        )