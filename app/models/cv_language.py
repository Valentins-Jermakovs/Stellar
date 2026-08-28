# SQLAlchemy column and foreign key definitions.
from sqlalchemy import Column, ForeignKey

# Field definitions and the base class for SQLModel database models.
from sqlmodel import Field, SQLModel


class CVLanguage(SQLModel, table=True):
    """Store the association between a CV and a language."""

    __tablename__ = "cv_language"

    # ID of the CV.
    # Together with language_id, it forms the composite primary key.
    # Delete the association when the CV is deleted.
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

    # ID of the language.
    # Together with cv_id, it forms the composite primary key.
    language_id: int = Field(
        foreign_key="language.id",
        primary_key=True,
    )

    # Language proficiency specified for this CV.
    proficiency: str = Field(
        max_length=50,
    )

    # Position used to preserve the order of languages in the CV.
    sort_order: int = 0