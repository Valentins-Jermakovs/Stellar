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

from app.facades import CVProjectFacade

from app.schemas import (
    CVProjectCreate,
    CVProjectRead,
    CVProjectUpdate,
)


# ==============================
# Router dependencies
# ==============================

from .dependencies import (
    get_project_facade,
    jwt_auth,
)


# ==============================
# CV project router
# ==============================

router = APIRouter(
    prefix="/cvs/{cv_id}/projects",
    tags=["CV Projects"],
)


# Create a new project for a CV.
@router.post(
    "",
    response_model=CVProjectRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    cv_id: int,
    data: CVProjectCreate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVProjectFacade = Depends(
        get_project_facade
    ),
):
    """
    Create a new project for a CV.
    """

    return await facade.create(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


# Update an existing project.
@router.patch(
    "/{project_id}",
    response_model=CVProjectRead,
)
async def update_project(
    cv_id: int,
    project_id: int,
    data: CVProjectUpdate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVProjectFacade = Depends(
        get_project_facade
    ),
):
    """
    Update an existing project.
    """

    return await facade.update(
        project_id=project_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


# Delete an existing project.
@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    cv_id: int,
    project_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVProjectFacade = Depends(
        get_project_facade
    ),
):
    """
    Delete an existing project.
    """

    await facade.delete(
        project_id=project_id,
        user_id=int(current_user["sub"]),
    )