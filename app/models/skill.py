from sqlmodel import Field, SQLModel


class Skill(SQLModel, table=True):
    """Reusable skill that can be assigned to multiple CVs."""

    __tablename__ = "skill"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    name: str = Field(
        max_length=100,
        unique=True,
        index=True,
    )