# Field definitions and the base class for SQLModel database models.
from sqlmodel import Field, SQLModel


class CVPersonalInfo(SQLModel, table=True):
    """Store personal information displayed on a CV."""

    __tablename__ = "cv_personal_info"

    # Automatically generated primary key.
    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # ID of the CV this information belongs to.
    cv_id: int = Field(
        foreign_key="cv.id",
        index=True,
    )

    # User's first name.
    first_name: str = Field(
        max_length=100,
    )

    # User's last name.
    last_name: str = Field(
        max_length=100,
    )

    # Short professional headline shown below the user's name.
    headline: str | None = Field(
        default=None,
        max_length=200,
    )

    # Contact email displayed on the CV.
    email: str | None = Field(
        default=None,
        max_length=255,
    )

    # Contact phone number.
    phone: str | None = Field(
        default=None,
        max_length=50,
    )

    # User's location.
    location: str | None = Field(
        default=None,
        max_length=150,
    )

    # Personal or professional website.
    website: str | None = Field(
        default=None,
        max_length=500,
    )

    # LinkedIn profile URL.
    linkedin: str | None = Field(
        default=None,
        max_length=500,
    )

    # GitHub profile URL.
    github: str | None = Field(
        default=None,
        max_length=500,
    )

    # Optional professional summary.
    summary: str | None = None