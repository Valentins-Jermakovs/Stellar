# ==============================
# Library imports
# ==============================

from typing import (
    Generic,
    TypeVar,
)

from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import (
    SQLModel,
    select,
)


# ==============================
# Repository types
# ==============================

# Type used by the generic repository.
# It can be any SQLModel-based entity.
ModelType = TypeVar(
    "ModelType",
    bound=SQLModel,
)


# ==============================
# Base repository
# ==============================

class BaseRepository(Generic[ModelType]):
    """
    Provide common CRUD operations for SQLModel entities.
    """

    model: type[ModelType]

    def __init__(
        self,
        session: AsyncSession,
    ):
        """
        Initialize the repository with a database session.
        """

        self.session = session

    async def create(
        self,
        instance: ModelType,
    ) -> ModelType:
        """
        Persist a new entity and return the refreshed instance.
        """

        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)

        return instance

    async def get_by_id(
        self,
        instance_id: int,
    ) -> ModelType | None:
        """
        Return an entity by primary key, if it exists.
        """

        result = await self.session.execute(
            select(self.model).where(
                self.model.id == instance_id,
            )
        )

        return result.scalar_one_or_none()

    async def update(
        self,
        instance: ModelType,
    ) -> ModelType:
        """
        Flush changes and return the refreshed entity.
        """

        await self.session.flush()
        await self.session.refresh(instance)

        return instance

    async def delete(
        self,
        instance: ModelType,
    ) -> None:
        """
        Delete an entity from the database.
        """

        await self.session.delete(instance)
        await self.session.flush()