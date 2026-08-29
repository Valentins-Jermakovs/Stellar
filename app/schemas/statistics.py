# ==============================
# Library imports
# ==============================

from pydantic import BaseModel


# ==============================
# CV statistics schemas
# ==============================

class CVStatistics(BaseModel):

    total_cvs: int

    total_experience: int
    total_education: int
    total_projects: int
    total_skills: int
    total_languages: int
    total_certifications: int