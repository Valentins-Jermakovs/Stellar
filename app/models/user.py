# Used for storing the time when the user reference was created.
from datetime import datetime, timezone

# Field definitions and the base class for SQLModel models.
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Return the current UTC time without timezone information."""
    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=None
    )


class User(SQLModel, table=True):
    """
    Store a local reference to an authenticated user.

    The user ID is obtained from the JWT token and is used to associate
    application data, such as CVs, with the corresponding user.
    """

    __tablename__ = "user"

    # User ID received from the authentication service through the JWT.
    id: int = Field(
        primary_key=True,
    )

    # Store when the local user reference was first created.
    created_at: datetime = Field(
        default_factory=utc_now,
    )