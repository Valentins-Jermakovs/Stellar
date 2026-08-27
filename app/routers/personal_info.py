from fastapi import APIRouter, Depends, status

from facades import CVPersonalInfoFacade
from schemas import (
    CVPersonalInfoCreate,
    CVPersonalInfoRead,
    CVPersonalInfoUpdate,
)

from .dependencies import (
    get_personal_info_facade,
    jwt_auth,
)


router = APIRouter(
    prefix="/cvs/{cv_id}/personal-info",
    tags=["CV Personal Info"],
)


@router.post(
    "",
    response_model=CVPersonalInfoRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_personal_info(
    cv_id: int,
    data: CVPersonalInfoCreate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVPersonalInfoFacade = Depends(
        get_personal_info_facade
    ),
):
    return await facade.create(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.get(
    "",
    response_model=CVPersonalInfoRead,
)
async def get_personal_info(
    cv_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVPersonalInfoFacade = Depends(
        get_personal_info_facade
    ),
):
    return await facade.get_by_cv_id(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
    )


@router.patch(
    "",
    response_model=CVPersonalInfoRead,
)
async def update_personal_info(
    cv_id: int,
    data: CVPersonalInfoUpdate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVPersonalInfoFacade = Depends(
        get_personal_info_facade
    ),
):
    return await facade.update(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_personal_info(
    cv_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVPersonalInfoFacade = Depends(
        get_personal_info_facade
    ),
):
    await facade.delete(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
    )