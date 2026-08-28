from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Return the current UTC time without timezone information."""
    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=None
    )


class User(SQLModel, table=True):
    """Application user who can own CVs."""

    __tablename__ = "user"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    username: str = Field(
        max_length=100,
        unique=True,
        index=True,
    )

    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
    )

    password_hash: str = Field(
        max_length=255,
    )

    created_at: datetime = Field(
        default_factory=utc_now,
    )