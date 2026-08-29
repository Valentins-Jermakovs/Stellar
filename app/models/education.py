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
# CV education model
# ==============================

class CVEducation(SQLModel, table=True):
    """
    Store an education entry included in a CV.
    """

    __tablename__ = "cv_education"

    __table_args__ = (
        UniqueConstraint(
            "cv_id",
            "institution",
            "degree",
            "field_of_study",
            "start_date",
            name="uq_cv_education",
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

    # ID of the CV this education entry belongs to.
    # The education entry is deleted when the CV is deleted.
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
    # Education information
    # ==============================

    # Name of the educational institution.
    institution: str = Field(
        max_length=250,
    )

    # Degree or qualification obtained at the institution.
    degree: str | None = Field(
        default=None,
        max_length=200,
    )

    # Field or subject area studied by the user.
    field_of_study: str | None = Field(
        default=None,
        max_length=200,
    )

    # Location of the educational institution.
    location: str | None = Field(
        default=None,
        max_length=150,
    )

    # Date when the education started.
    start_date: date | None = None

    # Date when the education ended.
    end_date: date | None = None

    # Optional description of the education or related achievements.
    description: str | None = None

    # ==============================
    # Display settings
    # ==============================

    # Position used to preserve the order of education entries in the CV.
    sort_order: int = 0