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
    redis: Redis = Depends(get_redis),
) -> CVPersonalInfoFacade:
    """Create a personal information facade with database and Redis dependencies."""
    return CVPersonalInfoFacade(
        session=session,
        redis=redis,
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
    redis: Redis = Depends(get_redis),
) -> CVEducationFacade:
    """Create an education facade with database and Redis dependencies."""
    return CVEducationFacade(
        session=session,
        redis=redis,
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
    redis: Redis = Depends(get_redis),
) -> CVSkillFacade:
    """Create a CV skill facade with database and Redis dependencies."""
    return CVSkillFacade(
        session=session,
        redis=redis,
    )


def get_project_facade(
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> CVProjectFacade:
    """Create a project facade with database and Redis dependencies."""
    return CVProjectFacade(
        session=session,
        redis=redis,
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
    redis: Redis = Depends(get_redis),
) -> CVLanguageFacade:
    """Create a CV language facade with database and Redis dependencies."""
    return CVLanguageFacade(
        session=session,
        redis=redis,
    )


def get_certification_facade(
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> CVCertificationFacade:
    """Create a certification facade with database and Redis dependencies."""
    return CVCertificationFacade(
        session=session,
        redis=redis,
    )


def get_generator_facade(
    session: AsyncSession = Depends(get_session),
) -> CVGeneratorFacade:
    """Create a CV generator facade."""
    return CVGeneratorFacade(
        session=session,
        templates_path=TEMPLATES_DIR,
    )