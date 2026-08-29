# ==============================
# Library imports
# ==============================

from datetime import date

from sqlalchemy import (
    Column,
    ForeignKey,
    UniqueConstraint,
)

from sqlmodel import Field, SQLModel


# ==============================
# CV experience model
# ==============================

class CVExperience(SQLModel, table=True):
    """
    Store a work experience entry included in a CV.
    """

    __tablename__ = "cv_experience"

    __table_args__ = (
        UniqueConstraint(
            "cv_id",
            "company",
            "position",
            "start_date",
            name="uq_cv_experience",
        ),
    )

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

    # ID of the CV this experience entry belongs to.
    # The experience entry is deleted when the CV is deleted.
    cv_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "cv.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        ),
    )

    # ==============================
    # Employment information
    # ==============================

    # Name of the company or organization.
    company: str = Field(
        max_length=200,
    )

    # Job title or position held by the user.
    position: str = Field(
        max_length=200,
    )

    # Location where the user worked.
    location: str | None = Field(
        default=None,
        max_length=150,
    )

    # Date when the employment started.
    start_date: date

    # Date when the employment ended.
    end_date: date | None = None

    # Indicates whether the user currently holds this position.
    is_current: bool = False

    # Optional description of the user's responsibilities and achievements.
    description: str | None = None

    # ==============================
    # Display settings
    # ==============================

    # Position used to preserve the order of experience entries in the CV.
    sort_order: int = 0