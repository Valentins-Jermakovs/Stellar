from sqlmodel import Field, SQLModel


class CVPersonalInfo(SQLModel, table=True):
    """Personal information displayed in a CV."""

    __tablename__ = "cv_personal_info"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    cv_id: int = Field(
        foreign_key="cv.id",
        index=True,
    )

    first_name: str = Field(
        max_length=100,
    )

    last_name: str = Field(
        max_length=100,
    )

    headline: str | None = Field(
        default=None,
        max_length=200,
    )

    email: str | None = Field(
        default=None,
        max_length=255,
    )

    phone: str | None = Field(
        default=None,
        max_length=50,
    )

    location: str | None = Field(
        default=None,
        max_length=150,
    )

    website: str | None = Field(
        default=None,
        max_length=500,
    )

    linkedin: str | None = Field(
        default=None,
        max_length=500,
    )

    github: str | None = Field(
        default=None,
        max_length=500,
    )

    summary: str | None = None