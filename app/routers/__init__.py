from fastapi import APIRouter

from .certification import router as certification_router
from .cv import router as cv_router
from .education import router as education_router
from .experience import router as experience_router
from .generator import router as generator_router
from .language import router as language_router
from .personal_info import router as personal_info_router
from .project import router as project_router
from .skill import router as skill_router
from .statistics import router as statistics_router

main_router = APIRouter()


main_router.include_router(
    cv_router
)

main_router.include_router(
    personal_info_router
)

main_router.include_router(
    experience_router
)

main_router.include_router(
    education_router
)

main_router.include_router(
    skill_router
)

main_router.include_router(
    project_router
)

main_router.include_router(
    language_router
)

main_router.include_router(
    certification_router
)

main_router.include_router(
    generator_router
)

main_router.include_router(
    statistics_router
)