from fastapi import APIRouter, Depends, status

from facades import CVExperienceFacade
from schemas import (
    CVExperienceCreate,
    CVExperienceRead,
    CVExperienceUpdate,
)

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
    return await facade.create(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.get(
    "",
    response_model=list[CVExperienceRead],
)
async def get_experiences(
    cv_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVExperienceFacade = Depends(
        get_experience_facade
    ),
):
    return await facade.get_by_cv_id(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
    )


@router.get(
    "/{experience_id}",
    response_model=CVExperienceRead,
)
async def get_experience(
    experience_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVExperienceFacade = Depends(
        get_experience_facade
    ),
):
    return await facade.get_by_id(
        experience_id=experience_id,
        user_id=int(current_user["sub"]),
    )


@router.patch(
    "/{experience_id}",
    response_model=CVExperienceRead,
)
async def update_experience(
    experience_id: int,
    data: CVExperienceUpdate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVExperienceFacade = Depends(
        get_experience_facade
    ),
):
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
    experience_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVExperienceFacade = Depends(
        get_experience_facade
    ),
):
    await facade.delete(
        experience_id=experience_id,
        user_id=int(current_user["sub"]),
    )