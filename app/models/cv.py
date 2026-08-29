# ==============================
# Library imports
# ==============================

from datetime import (
    datetime,
    timezone,
)

from sqlmodel import Field, SQLModel


# ==============================
# Date and time utilities
# ==============================

def utc_now() -> datetime:
    """
    Return the current UTC time without timezone information.
    """

    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=None
    )


# ==============================
# CV model
# ==============================

class CV(SQLModel, table=True):
    """
    Store a CV belonging to a user.
    """

    __tablename__ = "cv"

    # ==============================
    # Primary key
    # ==============================

    # Automatically generated primary key.
    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # ==============================
    # User relationship
    # ==============================

    # ID of the user who owns the CV.
    user_id: int = Field(
        foreign_key="user.id",
        index=True,
    )

    # ==============================
    # CV information
    # ==============================

    # Unique CV title.
    title: str = Field(
        max_length=150,
        unique=True,
        index=True,
    )

    # ==============================
    # Timestamps
    # ==============================

    # Time when the CV was created.
    created_at: datetime = Field(
        default_factory=utc_now,
    )

    # Time when the CV was last updated.
    updated_at: datetime = Field(
        default_factory=utc_now,
    )