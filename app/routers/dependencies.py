from fastapi import Depends

from redis.asyncio import Redis

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session

from app.config.paths import TEMPLATES_DIR

from app.config.redis import get_redis

from app.config.settings import settings

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

from app.utils import JWTAuth, JWTManager


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
    return CVFacade(
        session=session,
        redis=redis,
    )


def get_personal_info_facade(
    session: AsyncSession = Depends(get_session),
) -> CVPersonalInfoFacade:
    return CVPersonalInfoFacade(
        session
    )


def get_experience_facade(
    session: AsyncSession = Depends(get_session),
) -> CVExperienceFacade:
    return CVExperienceFacade(
        session
    )


def get_education_facade(
    session: AsyncSession = Depends(get_session),
) -> CVEducationFacade:
    return CVEducationFacade(
        session
    )


def get_skill_facade(
    session: AsyncSession = Depends(get_session),
) -> SkillFacade:
    return SkillFacade(
        session
    )


def get_cv_skill_facade(
    session: AsyncSession = Depends(get_session),
) -> CVSkillFacade:
    return CVSkillFacade(
        session
    )


def get_project_facade(
    session: AsyncSession = Depends(get_session),
) -> CVProjectFacade:
    return CVProjectFacade(
        session
    )


def get_language_facade(
    session: AsyncSession = Depends(get_session),
) -> LanguageFacade:
    return LanguageFacade(
        session
    )


def get_cv_language_facade(
    session: AsyncSession = Depends(get_session),
) -> CVLanguageFacade:
    return CVLanguageFacade(
        session
    )


def get_certification_facade(
    session: AsyncSession = Depends(get_session),
) -> CVCertificationFacade:
    return CVCertificationFacade(
        session
    )


def get_generator_facade(
    session: AsyncSession = Depends(get_session),
) -> CVGeneratorFacade:
    return CVGeneratorFacade(
        session=session,
        templates_path=TEMPLATES_DIR,
    )