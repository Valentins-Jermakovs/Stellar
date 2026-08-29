# ==============================
# Library imports
# ==============================

from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import select


# ==============================
# Application imports
# ==============================

from app.models import User

from .base import BaseRepository


# ==============================
# User repository
# ==============================

class UserRepository(BaseRepository[User]):
    """
    Provide database operations for User entities.
    """

    model = User

    async def get_by_id(
        self,
        user_id: int,
    ) -> User | None:
        """
        Return a user by ID, if the user exists.
        """

        result = await self.session.execute(
            select(User).where(
                User.id == user_id
            )
        )

        return result.scalar_one_or_none()