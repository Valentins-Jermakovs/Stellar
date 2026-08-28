from datetime import date

from sqlmodel import Field, SQLModel


class CVEducation(SQLModel, table=True):
    """Education entry belonging to a CV."""

    __tablename__ = "cv_education"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    cv_id: int = Field(
        foreign_key="cv.id",
        index=True,
    )

    institution: str = Field(
        max_length=250,
    )

    degree: str | None = Field(
        default=None,
        max_length=200,
    )

    field_of_study: str | None = Field(
        default=None,
        max_length=200,
    )

    location: str | None = Field(
        default=None,
        max_length=150,
    )

    start_date: date | None = None

    end_date: date | None = None

    description: str | None = None

    sort_order: int = 0