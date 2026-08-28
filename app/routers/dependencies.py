# FastAPI dependency injection.
from fastapi import Depends

# Async Redis and PostgreSQL session types.
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

# Application configuration and dependencies.
from app.config.database import get_session
from app.config.paths import TEMPLATES_DIR
from app.config.redis import get_redis
from app.config.settings import settings

# Facades used by the API routers.
from app.facades import (
    CVCertificationFacade,
    CVEducationFacade,
    CVExperienceFacade,
    CVFacade,
    CVGeneratorFacade,
    CVLanguageFacade,
    CVPersonalInfoFacade,
    CVProjectFacade,
    CVSkillFacade,
    LanguageFacade,
    SkillFacade,
)

# Authentication utilities.
from app.utils import JWTAuth, JWTManager


# Shared JWT configuration used by the authentication dependency.
jwt_manager = JWTManager(
    secret_key=settings.JWT_SECRET_KEY,
    algorithm=settings.JWT_ALGORITHM,
)

jwt_auth = JWTAuth(
    jwt_manager=jwt_manager,
)


def get_cv_facade(
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> CVFacade:
    """Create a CV facade with database and Redis dependencies."""
    return CVFacade(
        session=session,
        redis=redis,
    )


def get_personal_info_facade(
    session: AsyncSession = Depends(get_session),
) -> CVPersonalInfoFacade:
    """Create a personal information facade."""
    return CVPersonalInfoFacade(
        session
    )


def get_experience_facade(
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> CVExperienceFacade:
    """Create an experience facade with database and Redis dependencies."""
    return CVExperienceFacade(
        session=session,
        redis=redis,
    )


def get_education_facade(
    session: AsyncSession = Depends(get_session),
) -> CVEducationFacade:
    """Create an education facade."""
    return CVEducationFacade(
        session
    )


def get_skill_facade(
    session: AsyncSession = Depends(get_session),
) -> SkillFacade:
    """Create a skill facade."""
    return SkillFacade(
        session
    )


def get_cv_skill_facade(
    session: AsyncSession = Depends(get_session),
) -> CVSkillFacade:
    """Create a CV skill facade."""
    return CVSkillFacade(
        session
    )


def get_project_facade(
    session: AsyncSession = Depends(get_session),
) -> CVProjectFacade:
    """Create a project facade."""
    return CVProjectFacade(
        session
    )


def get_language_facade(
    session: AsyncSession = Depends(get_session),
) -> LanguageFacade:
    """Create a language facade."""
    return LanguageFacade(
        session
    )


def get_cv_language_facade(
    session: AsyncSession = Depends(get_session),
) -> CVLanguageFacade:
    """Create a CV language facade."""
    return CVLanguageFacade(
        session
    )


def get_certification_facade(
    session: AsyncSession = Depends(get_session),
) -> CVCertificationFacade:
    """Create a certification facade."""
    return CVCertificationFacade(
        session
    )


def get_generator_facade(
    session: AsyncSession = Depends(get_session),
) -> CVGeneratorFacade:
    """Create a CV generator facade."""
    return CVGeneratorFacade(
        session=session,
        templates_path=TEMPLATES_DIR,
    )

