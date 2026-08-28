from datetime import date

from sqlmodel import Field, SQLModel


class CVExperience(SQLModel, table=True):
    """Work experience entry belonging to a CV."""

    __tablename__ = "cv_experience"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    cv_id: int = Field(
        foreign_key="cv.id",
        index=True,
    )

    company: str = Field(
        max_length=200,
    )

    position: str = Field(
        max_length=200,
    )

    location: str | None = Field(
        default=None,
        max_length=150,
    )

    start_date: date

    end_date: date | None = None

    is_current: bool = False

    description: str | None = None

    sort_order: int = 0