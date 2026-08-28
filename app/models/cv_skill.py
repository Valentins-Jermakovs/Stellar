# Field definitions and the base class for SQLModel database models.
from sqlmodel import Field, SQLModel


class CVSkill(SQLModel, table=True):
    """Store the association between a CV and a skill."""

    __tablename__ = "cv_skill"

    # ID of the CV.
    # Together with skill_id, it forms the composite primary key.
    cv_id: int = Field(
        foreign_key="cv.id",
        primary_key=True,
    )

    # ID of the skill.
    # Together with cv_id, it forms the composite primary key.
    skill_id: int = Field(
        foreign_key="skill.id",
        primary_key=True,
    )

    # Optional skill level specified for this CV.
    level: str | None = Field(
        default=None,
        max_length=50,
    )

    # Position used to preserve the order of skills in the CV.
    sort_order: int = 0