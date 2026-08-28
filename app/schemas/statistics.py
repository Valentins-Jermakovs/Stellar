from pydantic import BaseModel


class CVStatistics(BaseModel):
    """Return statistics for a user's CV data."""

    total_cvs: int

    total_experience: int
    total_education: int
    total_projects: int
    total_skills: int
    total_languages: int
    total_certifications: int