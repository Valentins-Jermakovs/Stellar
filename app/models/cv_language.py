from sqlmodel import Field, SQLModel


class CVLanguage(SQLModel, table=True):
    """Association between a CV and a language."""

    __tablename__ = "cv_language"

    cv_id: int = Field(
        foreign_key="cv.id",
        primary_key=True,
    )

    language_id: int = Field(
        foreign_key="language.id",
        primary_key=True,
    )

    proficiency: str = Field(
        max_length=50,
    )

    sort_order: int = 0