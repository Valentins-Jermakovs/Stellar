from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select


ModelType = TypeVar(
    "ModelType",
    bound=SQLModel,
)


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create(
        self,
        instance: ModelType,
    ) -> ModelType:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)

        return instance

    async def get_by_id(
        self,
        instance_id: int,
    ) -> ModelType | None:
        result = await self.session.execute(
            select(self.model).where(
                self.model.id == instance_id
            )
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        instance: ModelType,
    ) -> ModelType:
        await self.session.flush()
        await self.session.refresh(instance)

        return instance

    async def delete(
        self,
        instance: ModelType,
    ) -> None:
        await self.session.delete(instance)
        await self.session.flush()