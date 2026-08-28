from datetime import date

from sqlmodel import Field, SQLModel


class CVCertification(SQLModel, table=True):
    """Certification entry belonging to a CV."""

    __tablename__ = "cv_certification"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    cv_id: int = Field(
        foreign_key="cv.id",
        index=True,
    )

    name: str = Field(
        max_length=250,
    )

    organization: str | None = Field(
        default=None,
        max_length=250,
    )

    issue_date: date | None = None

    expiration_date: date | None = None

    credential_id: str | None = Field(
        default=None,
        max_length=150,
    )

    credential_url: str | None = Field(
        default=None,
        max_length=500,
    )

    sort_order: int = 0