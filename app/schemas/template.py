from enum import StrEnum

from pydantic import BaseModel


class CVTemplate(StrEnum):
    CLASSIC = "classic"
    MODERN = "modern"
    MINIMAL = "minimal"


class CVGenerateRequest(BaseModel):
    template: CVTemplate