# FastAPI routing and dependency injection.
from fastapi import APIRouter, Depends, status

from app.facades import CVEducationFacade

# Request and response schemas used by the endpoints.
from app.schemas import (
    CVEducationCreate,
    CVEducationRead,
    CVEducationUpdate,
)

# Dependencies shared by CV education endpoints.
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
    """Create a new education entry for a CV."""
    return await facade.create(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.patch(
    "/{education_id}",
    response_model=CVEducationRead,
)
async def update_education(
    cv_id: int,
    education_id: int,
    data: CVEducationUpdate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVEducationFacade = Depends(
        get_education_facade
    ),
):
    """Update an existing education entry."""
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
    cv_id: int,
    education_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVEducationFacade = Depends(
        get_education_facade
    ),
):
    """Delete an existing education entry."""
    await facade.delete(
        education_id=education_id,
        user_id=int(current_user["sub"]),
    )