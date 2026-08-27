from fastapi import APIRouter, Depends, status

from app.facades import CVFacade
from app.schemas import (
    CVCreate,
    CVRead,
    CVUpdate,
)

from .dependencies import (
    get_cv_facade,
    jwt_auth,
)


router = APIRouter(
    prefix="/cvs",
    tags=["CV"],
)


@router.post(
    "",
    response_model=CVRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_cv(
    data: CVCreate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVFacade = Depends(
        get_cv_facade
    ),
):
    return await facade.create(
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.get(
    "",
    response_model=list[CVRead],
)
async def get_my_cvs(
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVFacade = Depends(
        get_cv_facade
    ),
):
    return await facade.get_by_user_id(
        user_id=int(current_user["sub"]),
    )


@router.get(
    "/{cv_id}",
    response_model=CVRead,
)
async def get_cv(
    cv_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVFacade = Depends(
        get_cv_facade
    ),
):
    return await facade.get_by_id(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
    )


@router.patch(
    "/{cv_id}",
    response_model=CVRead,
)
async def update_cv(
    cv_id: int,
    data: CVUpdate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVFacade = Depends(
        get_cv_facade
    ),
):
    return await facade.update(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.delete(
    "/{cv_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_cv(
    cv_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVFacade = Depends(
        get_cv_facade
    ),
):
    await facade.delete(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
    )