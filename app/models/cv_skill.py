# ==============================
# Library imports
# ==============================

from sqlalchemy import (
    Column,
    ForeignKey,
)

from sqlmodel import Field, SQLModel


# ==============================
# CV skill model
# ==============================

class CVSkill(SQLModel, table=True):
    """
    Store the association between a CV and a skill.
    """

    __tablename__ = "cv_skill"

    # ==============================
    # CV relationship
    # ==============================

    # ID of the CV.
    # Together with skill_id, it forms the composite primary key.
    # The association is deleted when the CV is deleted.
    cv_id: int = Field(
        sa_column=Column(
            ForeignKey(
                "cv.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            primary_key=True,
        ),
    )

    # ==============================
    # Skill relationship
    # ==============================

    # ID of the skill.
    # Together with cv_id, it forms the composite primary key.
    skill_id: int = Field(
        foreign_key="skill.id",
        primary_key=True,
    )

    # ==============================
    # Skill information
    # ==============================

    # Optional skill level specified for this CV.
    level: str | None = Field(
        default=None,
        max_length=50,
    )

    # ==============================
    # Display settings
    # ==============================

    # Position used to preserve the order of skills in the CV.
    sort_order: int = 0