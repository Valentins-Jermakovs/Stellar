# FastAPI routing and dependency injection.
from fastapi import APIRouter, Depends, status

from app.facades import CVExperienceFacade

# Request and response schemas used by the endpoints.
from app.schemas import (
    CVExperienceCreate,
    CVExperienceRead,
    CVExperienceUpdate,
)

# Dependencies shared by CV experience endpoints.
from .dependencies import (
    get_experience_facade,
    jwt_auth,
)


router = APIRouter(
    prefix="/cvs/{cv_id}/experiences",
    tags=["CV Experience"],
)


@router.post(
    "",
    response_model=CVExperienceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_experience(
    cv_id: int,
    data: CVExperienceCreate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVExperienceFacade = Depends(
        get_experience_facade
    ),
):
    """Create a new work experience entry for a CV."""
    return await facade.create(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.patch(
    "/{experience_id}",
    response_model=CVExperienceRead,
)
async def update_experience(
    cv_id: int,
    experience_id: int,
    data: CVExperienceUpdate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVExperienceFacade = Depends(
        get_experience_facade
    ),
):
    """Update an existing work experience entry."""
    return await facade.update(
        experience_id=experience_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.delete(
    "/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_experience(
    cv_id: int,
    experience_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVExperienceFacade = Depends(
        get_experience_facade
    ),
):
    """Delete an existing work experience entry."""
    await facade.delete(
        experience_id=experience_id,
        user_id=int(current_user["sub"]),
    )