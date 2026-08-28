# Used for storing CV creation and update timestamps.
from datetime import datetime, timezone

# Field definitions and the base class for SQLModel database models.
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Return the current UTC time without timezone information."""
    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=None
    )


class CV(SQLModel, table=True):
    """Store a CV belonging to a user."""

    __tablename__ = "cv"

    # Automatically generated primary key.
    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # ID of the user who owns the CV.
    user_id: int = Field(
        foreign_key="user.id",
        index=True,
    )

    # Unique CV title.
    title: str = Field(
        max_length=150,
        unique=True,
        index=True,
    )

    # Time when the CV was created.
    created_at: datetime = Field(
        default_factory=utc_now,
    )

    # Time when the CV was last updated.
    updated_at: datetime = Field(
        default_factory=utc_now,
    )