# ==============================
# CV schemas
# ==============================

from .cv import (
    CVCreate,
    CVUpdate,
    CVRead,
    CVPersonalInfoCreate,
    CVPersonalInfoUpdate,
    CVPersonalInfoRead,
    CVExperienceCreate,
    CVExperienceUpdate,
    CVExperienceRead,
    CVEducationCreate,
    CVEducationUpdate,
    CVEducationRead,
    SkillCreate,
    SkillRead,
    CVSkillCreate,
    CVSkillUpdate,
    CVSkillRead,
    CVProjectCreate,
    CVProjectUpdate,
    CVProjectRead,
    LanguageCreate,
    LanguageRead,
    CVLanguageCreate,
    CVLanguageUpdate,
    CVLanguageRead,
    CVCertificationCreate,
    CVCertificationUpdate,
    CVCertificationRead,
    CVSkillDetailRead,
    CVLanguageDetailRead,
    CVDetailRead,
    CVPageRead,
)


# ==============================
# Document schemas
# ==============================

from .document import (
    CVDocument,
    CVDocumentLanguage,
    CVDocumentSkill,
)


# ==============================
# Template schemas
# ==============================

from .template import (
    CVGenerateRequest,
    CVTemplate,
    CVLocale,
)


# ==============================
# Statistics schemas
# ==============================

from .statistics import CVStatistics