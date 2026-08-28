from datetime import date

from sqlmodel import Field, SQLModel


class CVProject(SQLModel, table=True):
    """Project entry belonging to a CV."""

    __tablename__ = "cv_project"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    cv_id: int = Field(
        foreign_key="cv.id",
        index=True,
    )

    name: str = Field(
        max_length=200,
    )

    description: str | None = None

    url: str | None = Field(
        default=None,
        max_length=500,
    )

    github_url: str | None = Field(
        default=None,
        max_length=500,
    )

    start_date: date | None = None

    end_date: date | None = None

    sort_order: int = 0