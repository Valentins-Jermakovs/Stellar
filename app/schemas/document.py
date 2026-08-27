from pydantic import BaseModel

from .cv import (
    CVCertificationRead,
    CVEducationRead,
    CVExperienceRead,
    CVPersonalInfoRead,
    CVProjectRead,
)
from .template import CVTemplate


class CVDocumentSkill(BaseModel):
    id: int
    name: str
    level: str | None
    sort_order: int


class CVDocumentLanguage(BaseModel):
    id: int
    name: str
    proficiency: str
    sort_order: int


class CVDocument(BaseModel):
    cv_id: int
    user_id: int
    title: str

    personal_info: CVPersonalInfoRead | None
    experience: list[CVExperienceRead]
    education: list[CVEducationRead]
    skills: list[CVDocumentSkill]
    projects: list[CVProjectRead]
    languages: list[CVDocumentLanguage]
    certifications: list[CVCertificationRead]

    template: CVTemplate