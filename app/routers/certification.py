# ==============================
# Library imports
# ==============================

from fastapi import (
    APIRouter,
    Depends,
    status,
)


# ==============================
# Application imports
# ==============================

from app.facades import CVCertificationFacade

from app.schemas import (
    CVCertificationCreate,
    CVCertificationRead,
    CVCertificationUpdate,
)


# ==============================
# Router dependencies
# ==============================

from .dependencies import (
    get_certification_facade,
    jwt_auth,
)


# ==============================
# CV certification router
# ==============================

router = APIRouter(
    prefix="/cvs/{cv_id}/certifications",
    tags=["CV Certifications"],
)


# Create a new certification for a CV.
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
    """
    Create a certification for a CV.
    """

    return await facade.create(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


# Update an existing certification.
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
    """
    Update an existing certification.
    """

    return await facade.update(
        certification_id=certification_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


# Delete an existing certification.
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
    """
    Delete an existing certification.
    """

    await facade.delete(
        certification_id=certification_id,
        user_id=int(current_user["sub"]),
    )