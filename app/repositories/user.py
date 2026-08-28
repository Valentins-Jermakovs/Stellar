# Async database session used by the repository.
from sqlalchemy.ext.asyncio import AsyncSession

# SQL query builder for retrieving database records.
from sqlmodel import select

from app.models import User

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User-related database operations."""

    model = User

    async def get_by_id(
        self,
        user_id: int,
    ) -> User | None:
        """Return a user by ID, or None if the user does not exist."""
        result = await self.session.execute(
            select(User).where(
                User.id == user_id
            )
        )

        return result.scalar_one_or_none()