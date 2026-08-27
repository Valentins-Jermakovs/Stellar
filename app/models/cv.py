from datetime import date, datetime, timezone

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=None
    )


class CV(SQLModel, table=True):
    __tablename__ = "cv"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    user_id: int = Field(
        index=True,
    )

    title: str = Field(
        max_length=150,
    )

    created_at: datetime = Field(
        default_factory=utc_now,
    )

    updated_at: datetime = Field(
        default_factory=utc_now,
    )


class CVPersonalInfo(SQLModel, table=True):
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


class CVExperience(SQLModel, table=True):
    __tablename__ = "cv_experience"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    cv_id: int = Field(
        foreign_key="cv.id",
        index=True,
    )

    company: str = Field(
        max_length=200,
    )

    position: str = Field(
        max_length=200,
    )

    location: str | None = Field(
        default=None,
        max_length=150,
    )

    start_date: date

    end_date: date | None = None

    is_current: bool = False

    description: str | None = None

    sort_order: int = 0


class CVEducation(SQLModel, table=True):
    __tablename__ = "cv_education"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    cv_id: int = Field(
        foreign_key="cv.id",
        index=True,
    )

    institution: str = Field(
        max_length=250,
    )

    degree: str | None = Field(
        default=None,
        max_length=200,
    )

    field_of_study: str | None = Field(
        default=None,
        max_length=200,
    )

    location: str | None = Field(
        default=None,
        max_length=150,
    )

    start_date: date | None = None

    end_date: date | None = None

    description: str | None = None

    sort_order: int = 0


class Skill(SQLModel, table=True):
    __tablename__ = "skill"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    name: str = Field(
        max_length=100,
        unique=True,
        index=True,
    )


class CVSkill(SQLModel, table=True):
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


class CVProject(SQLModel, table=True):
    __tablename__ = "cv_project"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    cv_id: int = Field(
        foreign_key="cv.id",
        index=True,
    )

    name: str = Field(
        max_length=200,
    )

    description: str | None = None

    url: str | None = Field(
        default=None,
        max_length=500,
    )

    github_url: str | None = Field(
        default=None,
        max_length=500,
    )

    start_date: date | None = None

    end_date: date | None = None

    sort_order: int = 0


class Language(SQLModel, table=True):
    __tablename__ = "language"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    name: str = Field(
        max_length=100,
        unique=True,
        index=True,
    )


class CVLanguage(SQLModel, table=True):
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


class CVCertification(SQLModel, table=True):
    __tablename__ = "cv_certification"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    cv_id: int = Field(
        foreign_key="cv.id",
        index=True,
    )

    name: str = Field(
        max_length=250,
    )

    organization: str | None = Field(
        default=None,
        max_length=250,
    )

    issue_date: date | None = None

    expiration_date: date | None = None

    credential_id: str | None = Field(
        default=None,
        max_length=150,
    )

    credential_url: str | None = Field(
        default=None,
        max_length=500,
    )

    sort_order: int = 0