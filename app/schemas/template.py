# ==============================
# Library imports
# ==============================

from enum import StrEnum

from pydantic import BaseModel


# ==============================
# CV template enum
# ==============================

class CVTemplate(StrEnum):
    CLASSIC = "classic"
    MODERN = "modern"
    MINIMAL = "minimal"
    EXECUTIVE = "executive"
    EDITORIAL = "editorial"
    TIMELINE = "timeline"


# ==============================
# CV locale enum
# ==============================

class CVLocale(StrEnum):
    ENGLISH = "en"
    RUSSIAN = "ru"
    LATVIAN = "lv"


# ==============================
# CV generation schema
# ==============================

class CVGenerateRequest(BaseModel):
    template: CVTemplate
    language: CVLocale = CVLocale.ENGLISH