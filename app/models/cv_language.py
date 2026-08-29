# ==============================
# Library imports
# ==============================

from sqlalchemy import (
    Column,
    ForeignKey,
)

from sqlmodel import Field, SQLModel


# ==============================
# CV language model
# ==============================

class CVLanguage(SQLModel, table=True):
    """
    Store the association between a CV and a language.
    """

    __tablename__ = "cv_language"

    # ==============================
    # CV relationship
    # ==============================

    # ID of the CV.
    # Together with language_id, it forms the composite primary key.
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
    # Language relationship
    # ==============================

    # ID of the language.
    # Together with cv_id, it forms the composite primary key.
    language_id: int = Field(
        foreign_key="language.id",
        primary_key=True,
    )

    # ==============================
    # Language information
    # ==============================

    # Language proficiency specified for this CV.
    proficiency: str = Field(
        max_length=50,
    )

    # ==============================
    # Display settings
    # ==============================

    # Position used to preserve the order of languages in the CV.
    sort_order: int = 0