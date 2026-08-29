# ==============================
# Service imports
# ==============================

# CV core and related services.
from .certification import CVCertificationService
from .cv import CVService
from .education import CVEducationService
from .experience import CVExperienceService

from .language import (
    CVLanguageService,
    LanguageService,
)

from .personal_info import CVPersonalInfoService
from .project import CVProjectService

from .skill import (
    CVSkillService,
    SkillService,
)


# ==============================
# Supporting services
# ==============================

# CV ownership and document services.
from .document import CVDocumentService
from .ownership import CVOwnershipService


# ==============================
# Generation and statistics services
# ==============================

# CV generation service.
from .generator import CVGeneratorService

# CV statistics service.
from .statistics import StatisticsService