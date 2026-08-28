# FastAPI routing and dependency injection.
from fastapi import APIRouter, Depends, status

from app.facades import CVPersonalInfoFacade

# Request and response schemas used by the endpoints.
from app.schemas import (
    CVPersonalInfoCreate,
    CVPersonalInfoRead,
    CVPersonalInfoUpdate,
)

# Dependencies shared by CV personal information endpoints.
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
    """Create personal information for a CV."""
    return await facade.create(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
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
    """Update personal information for a CV."""
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
    """Delete personal information from a CV."""
    await facade.delete(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
    )