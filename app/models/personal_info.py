# ==============================
# Library imports
# ==============================

from sqlalchemy import (
    Column,
    ForeignKey,
)

from sqlmodel import Field, SQLModel


# ==============================
# CV personal information model
# ==============================

class CVPersonalInfo(SQLModel, table=True):
    """
    Store personal information displayed on a CV.
    """

    __tablename__ = "cv_personal_info"

    # ==============================
    # Primary key
    # ==============================

    # Automatically generated primary key.
    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # ==============================
    # CV relationship
    # ==============================

    # ID of the CV this information belongs to.
    # The personal information is deleted when the CV is deleted.
    cv_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "cv.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            unique=True,
            index=True,
        ),
    )

    # ==============================
    # Personal information
    # ==============================

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

    # ==============================
    # Contact information
    # ==============================

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

    # ==============================
    # Online profiles
    # ==============================

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

    # ==============================
    # Professional summary
    # ==============================

    # Optional professional summary.
    summary: str | None = None