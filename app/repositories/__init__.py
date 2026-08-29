# ==============================
# Base repository
# ==============================

from .base import BaseRepository


# ==============================
# Cache repository
# ==============================

from .cache import CacheRepository


# ==============================
# CV repositories
# ==============================

from .cv import (
    CVCertificationRepository,
    CVEducationRepository,
    CVExperienceRepository,
    CVLanguageRepository,
    CVPersonalInfoRepository,
    CVProjectRepository,
    CVRepository,
    CVSkillRepository,
    LanguageRepository,
    SkillRepository,
)


# ==============================
# User repository
# ==============================

from .user import UserRepository


# ==============================
# Statistics repository
# ==============================

from .statistics import StatisticsRepository