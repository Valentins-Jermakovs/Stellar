from fastapi import APIRouter, Depends, status

from facades import CVCertificationFacade
from schemas import (
    CVCertificationCreate,
    CVCertificationRead,
    CVCertificationUpdate,
)

from .dependencies import (
    get_certification_facade,
    jwt_auth,
)


router = APIRouter(
    prefix="/cvs/{cv_id}/certifications",
    tags=["CV Certifications"],
)


@router.post(
    "",
    response_model=CVCertificationRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_certification(
    cv_id: int,
    data: CVCertificationCreate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVCertificationFacade = Depends(
        get_certification_facade
    ),
):
    return await facade.create(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.get(
    "",
    response_model=list[CVCertificationRead],
)
async def get_certifications(
    cv_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVCertificationFacade = Depends(
        get_certification_facade
    ),
):
    return await facade.get_by_cv_id(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
    )


@router.get(
    "/{certification_id}",
    response_model=CVCertificationRead,
)
async def get_certification(
    certification_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVCertificationFacade = Depends(
        get_certification_facade
    ),
):
    return await facade.get_by_id(
        certification_id=certification_id,
        user_id=int(current_user["sub"]),
    )


@router.patch(
    "/{certification_id}",
    response_model=CVCertificationRead,
)
async def update_certification(
    certification_id: int,
    data: CVCertificationUpdate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVCertificationFacade = Depends(
        get_certification_facade
    ),
):
    return await facade.update(
        certification_id=certification_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.delete(
    "/{certification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_certification(
    certification_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVCertificationFacade = Depends(
        get_certification_facade
    ),
):
    await facade.delete(
        certification_id=certification_id,
        user_id=int(current_user["sub"]),
    )