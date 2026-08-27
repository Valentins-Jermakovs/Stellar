from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class TokenResponse:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@dataclass(slots=True)
class User:
    id: int
    username: str
    full_name: str
    email: str
    roles: list[str]
    is_active: bool
    created_at: datetime