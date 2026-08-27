from fastapi import APIRouter, Depends, status

from facades import CVEducationFacade
from schemas import (
    CVEducationCreate,
    CVEducationRead,
    CVEducationUpdate,
)

from .dependencies import (
    get_education_facade,
    jwt_auth,
)


router = APIRouter(
    prefix="/cvs/{cv_id}/education",
    tags=["CV Education"],
)


@router.post(
    "",
    response_model=CVEducationRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_education(
    cv_id: int,
    data: CVEducationCreate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVEducationFacade = Depends(
        get_education_facade
    ),
):
    return await facade.create(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.get(
    "",
    response_model=list[CVEducationRead],
)
async def get_education(
    cv_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVEducationFacade = Depends(
        get_education_facade
    ),
):
    return await facade.get_by_cv_id(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
    )


@router.get(
    "/{education_id}",
    response_model=CVEducationRead,
)
async def get_education_by_id(
    education_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVEducationFacade = Depends(
        get_education_facade
    ),
):
    return await facade.get_by_id(
        education_id=education_id,
        user_id=int(current_user["sub"]),
    )


@router.patch(
    "/{education_id}",
    response_model=CVEducationRead,
)
async def update_education(
    education_id: int,
    data: CVEducationUpdate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVEducationFacade = Depends(
        get_education_facade
    ),
):
    return await facade.update(
        education_id=education_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.delete(
    "/{education_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_education(
    education_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVEducationFacade = Depends(
        get_education_facade
    ),
):
    await facade.delete(
        education_id=education_id,
        user_id=int(current_user["sub"]),
    )