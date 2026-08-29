# ==============================
# Library imports
# ==============================

from sqlmodel import Field, SQLModel


# ==============================
# Skill model
# ==============================

class Skill(SQLModel, table=True):
    """
    Store a reusable skill that can be associated with CVs.
    """

    __tablename__ = "skill"

    # ==============================
    # Primary key
    # ==============================

    # Automatically generated primary key.
    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # ==============================
    # Skill information
    # ==============================

    # Skill name must be unique to avoid duplicate entries.
    name: str = Field(
        max_length=100,
        unique=True,
        index=True,
    )