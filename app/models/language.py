from sqlmodel import Field, SQLModel


class Language(SQLModel, table=True):
    """Reusable language that can be assigned to multiple CVs."""

    __tablename__ = "language"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    name: str = Field(
        max_length=100,
        unique=True,
        index=True,
    )