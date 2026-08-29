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
# CV project model
# ==============================

class CVProject(SQLModel, table=True):
    """
    Store a project included in a CV.
    """

    __tablename__ = "cv_project"

    __table_args__ = (
        UniqueConstraint(
            "cv_id",
            "name",
            name="uq_cv_project",
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

    # ID of the CV this project belongs to.
    # The project is deleted when the CV is deleted.
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
    # Project information
    # ==============================

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

    # ==============================
    # Project timeline
    # ==============================

    # Optional project start date.
    start_date: date | None = None

    # Optional project end date.
    end_date: date | None = None

    # ==============================
    # Display settings
    # ==============================

    # Position used to preserve the order of projects in the CV.
    sort_order: int = 0