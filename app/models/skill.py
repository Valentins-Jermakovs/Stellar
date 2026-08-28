# Field definitions and the base class for SQLModel database models.
from sqlmodel import Field, SQLModel


class Skill(SQLModel, table=True):
    """Store a reusable skill that can be associated with CVs."""

    __tablename__ = "skill"

    # Automatically generated primary key.
    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # Skill name must be unique so the same skill is not stored multiple times.
    name: str = Field(
        max_length=100,
        unique=True,
        index=True,
    )