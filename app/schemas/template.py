from enum import StrEnum

from pydantic import BaseModel


class CVTemplate(StrEnum):
    CLASSIC = "classic"
    MODERN = "modern"
    MINIMAL = "minimal"
    EXECUTIVE = "executive"
    EDITORIAL = "editorial"
    TIMELINE = "timeline"


class CVLocale(StrEnum):
    ENGLISH = "en"
    RUSSIAN = "ru"
    LATVIAN = "lv"


class CVGenerateRequest(BaseModel):
    template: CVTemplate
    language: CVLocale = CVLocale.ENGLISH

