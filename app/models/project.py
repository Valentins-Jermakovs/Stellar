# Used for storing project start and end dates.
from datetime import date

# SQLAlchemy column and foreign key definitions.
from sqlalchemy import Column, ForeignKey, UniqueConstraint

# Field definitions and the base class for SQLModel database models.
from sqlmodel import Field, SQLModel


class CVProject(SQLModel, table=True):
    """Store a project included in a CV."""

    __tablename__ = "cv_project"

    __table_args__ = (
        UniqueConstraint(
            "cv_id",
            "name",
            name="uq_cv_project",
        ),
    )

    # Automatically generated primary key.
    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # ID of the CV this project belongs to.
    # Delete the project automatically when the CV is deleted.
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

    # Project name.
    name: str = Field(
        max_length=200,
    )

    # Optional description of the project.
    description: str | None = None

    # Optional project URL.
    url: str | None = Field(
        default=None,
        max_length=500,
    )

    # Optional GitHub repository URL.
    github_url: str | None = Field(
        default=None,
        max_length=500,
    )

    # Optional project start date.
    start_date: date | None = None

    # Optional project end date.
    end_date: date | None = None

    # Position used to preserve the order of projects in the CV.
    sort_order: int = 0