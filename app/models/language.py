# ==============================
# Library imports
# ==============================

from sqlmodel import Field, SQLModel


# ==============================
# Language model
# ==============================

class Language(SQLModel, table=True):
    """
    Store a reusable language that can be associated with CVs.
    """

    __tablename__ = "language"

    # ==============================
    # Primary key
    # ==============================

    # Automatically generated primary key.
    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # ==============================
    # Language information
    # ==============================

    # Language name must be unique to avoid duplicate entries.
    name: str = Field(
        max_length=100,
        unique=True,
        index=True,
    )