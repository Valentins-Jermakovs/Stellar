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
# CV certification model
# ==============================

class CVCertification(SQLModel, table=True):
    """
    Store a certification included in a CV.
    """

    __tablename__ = "cv_certification"

    __table_args__ = (
        UniqueConstraint(
            "cv_id",
            "name",
            name="uq_cv_certification",
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

    # ID of the CV this certification belongs to.
    # The certification is deleted when the CV is deleted.
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
    # Certification information
    # ==============================

    # Name of the certification.
    name: str = Field(
        max_length=250,
    )

    # Organization that issued the certification.
    organization: str | None = Field(
        default=None,
        max_length=250,
    )

    # Date when the certification was issued.
    issue_date: date | None = None

    # Date when the certification expires, if applicable.
    expiration_date: date | None = None

    # Optional identifier assigned to the certification.
    credential_id: str | None = Field(
        default=None,
        max_length=150,
    )

    # Optional URL where the certification can be verified.
    credential_url: str | None = Field(
        default=None,
        max_length=500,
    )

    # ==============================
    # Display settings
    # ==============================

    # Position used to preserve the order of certifications in the CV.
    sort_order: int = 0