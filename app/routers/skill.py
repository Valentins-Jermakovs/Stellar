# FastAPI routing and dependency injection.
from fastapi import APIRouter, Depends, Query, status

from app.facades import (
    CVSkillFacade,
    SkillFacade,
)

# Request and response schemas used by the endpoints.
from app.schemas import (
    CVSkillCreate,
    CVSkillRead,
    CVSkillUpdate,
    SkillCreate,
    SkillRead,
)

# Dependencies shared by skill endpoints.
from .dependencies import (
    get_cv_skill_facade,
    get_skill_facade,
    jwt_auth,
)


router = APIRouter(
    tags=["Skills"],
)


@router.post(
    "/skills",
    response_model=SkillRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_skill(
    data: SkillCreate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: SkillFacade = Depends(
        get_skill_facade
    ),
):
    """Create a global skill."""
    return await facade.create(
        data
    )


@router.get(
    "/skills",
    response_model=list[SkillRead],
)
async def search_skills(
    query: str | None = Query(
        default=None,
        description="Search skills by name",
    ),
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: SkillFacade = Depends(
        get_skill_facade
    ),
):
    """Return up to ten global skills matching the query."""
    return await facade.search(
        query=query
    )


@router.get(
    "/skills/{skill_id}",
    response_model=SkillRead,
)
async def get_skill(
    skill_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: SkillFacade = Depends(
        get_skill_facade
    ),
):
    """Return a global skill by ID."""
    return await facade.get_by_id(
        skill_id
    )


@router.post(
    "/cvs/{cv_id}/skills",
    response_model=CVSkillRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_skill_to_cv(
    cv_id: int,
    data: CVSkillCreate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVSkillFacade = Depends(
        get_cv_skill_facade
    ),
):
    """Add a global skill to a CV."""
    return await facade.add(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.patch(
    "/cvs/{cv_id}/skills/{skill_id}",
    response_model=CVSkillRead,
)
async def update_cv_skill(
    cv_id: int,
    skill_id: int,
    data: CVSkillUpdate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVSkillFacade = Depends(
        get_cv_skill_facade
    ),
):
    """Update a skill association in a CV."""
    return await facade.update(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        skill_id=skill_id,
        data=data,
    )


@router.delete(
    "/cvs/{cv_id}/skills/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_cv_skill(
    cv_id: int,
    skill_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVSkillFacade = Depends(
        get_cv_skill_facade
    ),
):
    """Delete a skill association from a CV."""
    await facade.delete(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        skill_id=skill_id,
    )