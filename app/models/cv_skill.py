from sqlmodel import Field, SQLModel


class CVSkill(SQLModel, table=True):
    """Association between a CV and a skill."""

    __tablename__ = "cv_skill"

    cv_id: int = Field(
        foreign_key="cv.id",
        primary_key=True,
    )

    skill_id: int = Field(
        foreign_key="skill.id",
        primary_key=True,
    )

    level: str | None = Field(
        default=None,
        max_length=50,
    )

    sort_order: int = 0