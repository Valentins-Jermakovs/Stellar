# Used for storing certification issue and expiration dates.
from datetime import date

# Field definitions and the base class for SQLModel database models.
from sqlmodel import Field, SQLModel


class CVCertification(SQLModel, table=True):
    """Store a certification included in a CV."""

    __tablename__ = "cv_certification"

    # Automatically generated primary key.
    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # ID of the CV this certification belongs to.
    cv_id: int = Field(
        foreign_key="cv.id",
        index=True,
    )

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

    # Position used to preserve the order of certifications in the CV.
    sort_order: int = 0