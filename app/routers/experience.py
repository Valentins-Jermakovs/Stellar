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

from app.facades import CVExperienceFacade

from app.schemas import (
    CVExperienceCreate,
    CVExperienceRead,
    CVExperienceUpdate,
)

from .dependencies import (
    get_experience_facade,
    jwt_auth,
)


# ==============================
# Router configuration
# ==============================

router = APIRouter(
    prefix="/cvs/{cv_id}/experiences",
    tags=["CV Experience"],
)


# ==============================
# Create experience
# ==============================

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
    """
    Create a new work experience entry for a CV.

    The authenticated user's ID is extracted from the JWT token
    and passed to the facade together with the CV ID and request data.
    """
    return await facade.create(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


# ==============================
# Update experience
# ==============================

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
    """
    Update an existing work experience entry.

    The authenticated user's ID is passed to the facade
    to ensure that the experience entry belongs to the user.
    """
    return await facade.update(
        experience_id=experience_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


# ==============================
# Delete experience
# ==============================

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
    """
    Delete an existing work experience entry.

    The authenticated user's ID is passed to the facade
    to ensure that the experience entry belongs to the user.
    """
    await facade.delete(
        experience_id=experience_id,
        user_id=int(current_user["sub"]),
    )