from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


# ==============================
# CV Schemas
# ==============================

class CVCreate(BaseModel):
    title: str


class CVUpdate(BaseModel):
    title: str | None = None


class CVRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime


# ==============================
# Personal Information Schemas
# ==============================

class CVPersonalInfoCreate(BaseModel):
    first_name: str
    last_name: str

    headline: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None

    website: str | None = None
    linkedin: str | None = None
    github: str | None = None

    summary: str | None = None


class CVPersonalInfoUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None

    headline: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None

    website: str | None = None
    linkedin: str | None = None
    github: str | None = None

    summary: str | None = None


class CVPersonalInfoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cv_id: int

    first_name: str
    last_name: str

    headline: str | None
    email: str | None
    phone: str | None
    location: str | None

    website: str | None
    linkedin: str | None
    github: str | None

    summary: str | None


# ==============================
# Experience Schemas
# ==============================

class CVExperienceCreate(BaseModel):
    company: str
    position: str
    location: str | None = None

    start_date: date
    end_date: date | None = None
    is_current: bool = False

    description: str | None = None
    sort_order: int = 0


class CVExperienceUpdate(BaseModel):
    company: str | None = None
    position: str | None = None
    location: str | None = None

    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None

    description: str | None = None
    sort_order: int | None = None


class CVExperienceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cv_id: int

    company: str
    position: str
    location: str | None

    start_date: date
    end_date: date | None
    is_current: bool

    description: str | None
    sort_order: int


# ==============================
# Education Schemas
# ==============================

class CVEducationCreate(BaseModel):
    institution: str
    degree: str | None = None
    field_of_study: str | None = None
    location: str | None = None

    start_date: date | None = None
    end_date: date | None = None

    description: str | None = None
    sort_order: int = 0


class CVEducationUpdate(BaseModel):
    institution: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    location: str | None = None

    start_date: date | None = None
    end_date: date | None = None

    description: str | None = None
    sort_order: int | None = None


class CVEducationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cv_id: int

    institution: str
    degree: str | None
    field_of_study: str | None
    location: str | None

    start_date: date | None
    end_date: date | None

    description: str | None
    sort_order: int


# ==============================
# Skill Schemas
# ==============================

class SkillCreate(BaseModel):
    name: str


class SkillRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CVSkillCreate(BaseModel):
    skill_id: int
    level: str | None = None
    sort_order: int = 0


class CVSkillUpdate(BaseModel):
    level: str | None = None
    sort_order: int | None = None


class CVSkillRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cv_id: int
    skill_id: int
    level: str | None
    sort_order: int


# ==============================
# Project Schemas
# ==============================

class CVProjectCreate(BaseModel):
    name: str
    description: str | None = None

    url: str | None = None
    github_url: str | None = None

    start_date: date | None = None
    end_date: date | None = None

    sort_order: int = 0


class CVProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    url: str | None = None
    github_url: str | None = None

    start_date: date | None = None
    end_date: date | None = None

    sort_order: int | None = None


class CVProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cv_id: int

    name: str
    description: str | None

    url: str | None
    github_url: str | None

    start_date: date | None
    end_date: date | None

    sort_order: int


# ==============================
# Language Schemas
# ==============================

class LanguageCreate(BaseModel):
    name: str


class LanguageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CVLanguageCreate(BaseModel):
    language_id: int
    proficiency: str
    sort_order: int = 0


class CVLanguageUpdate(BaseModel):
    proficiency: str | None = None
    sort_order: int | None = None


class CVLanguageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cv_id: int
    language_id: int
    proficiency: str
    sort_order: int


# ==============================
# Certification Schemas
# ==============================

class CVCertificationCreate(BaseModel):
    name: str
    organization: str | None = None

    issue_date: date | None = None
    expiration_date: date | None = None

    credential_id: str | None = None
    credential_url: str | None = None

    sort_order: int = 0


class CVCertificationUpdate(BaseModel):
    name: str | None = None
    organization: str | None = None

    issue_date: date | None = None
    expiration_date: date | None = None

    credential_id: str | None = None
    credential_url: str | None = None

    sort_order: int | None = None


class CVCertificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cv_id: int

    name: str
    organization: str | None

    issue_date: date | None
    expiration_date: date | None

    credential_id: str | None
    credential_url: str | None

    sort_order: int



class CVSkillDetailRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

    level: str | None
    sort_order: int


class CVLanguageDetailRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

    proficiency: str
    sort_order: int


class CVDetailRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str

    created_at: datetime
    updated_at: datetime

    personal_info: CVPersonalInfoRead | None

    experience: list[CVExperienceRead]

    education: list[CVEducationRead]

    skills: list[CVSkillDetailRead]

    projects: list[CVProjectRead]

    languages: list[CVLanguageDetailRead]

    certifications: list[CVCertificationRead]


class CVPageRead(BaseModel):
    items: list[CVRead]

    total: int

    page: int
    page_size: int

    pages: int