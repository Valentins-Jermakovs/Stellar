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
# User model
# ==============================

class User(SQLModel, table=True):
    """
    Store a local reference to an authenticated user.

    The user ID is obtained from the JWT token and is used to associate
    application data, such as CVs, with the corresponding user.
    """

    __tablename__ = "user"

    # ==============================
    # Primary key
    # ==============================

    # User ID received from the authentication service through the JWT.
    id: int = Field(
        primary_key=True,
    )

    # ==============================
    # Timestamps
    # ==============================

    # Store when the local user reference was first created.
    created_at: datetime = Field(
        default_factory=utc_now,
    )