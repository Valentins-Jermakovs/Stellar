from fastapi import APIRouter, Depends, status

from app.facades import CVProjectFacade
from app.schemas import (
    CVProjectCreate,
    CVProjectRead,
    CVProjectUpdate,
)

from .dependencies import (
    get_project_facade,
    jwt_auth,
)


router = APIRouter(
    prefix="/cvs/{cv_id}/projects",
    tags=["CV Projects"],
)


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
    return await facade.create(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.get(
    "",
    response_model=list[CVProjectRead],
)
async def get_projects(
    cv_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVProjectFacade = Depends(
        get_project_facade
    ),
):
    return await facade.get_by_cv_id(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
    )


@router.get(
    "/{project_id}",
    response_model=CVProjectRead,
)
async def get_project(
    project_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVProjectFacade = Depends(
        get_project_facade
    ),
):
    return await facade.get_by_id(
        project_id=project_id,
        user_id=int(current_user["sub"]),
    )


@router.patch(
    "/{project_id}",
    response_model=CVProjectRead,
)
async def update_project(
    project_id: int,
    data: CVProjectUpdate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVProjectFacade = Depends(
        get_project_facade
    ),
):
    return await facade.update(
        project_id=project_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVProjectFacade = Depends(
        get_project_facade
    ),
):
    await facade.delete(
        project_id=project_id,
        user_id=int(current_user["sub"]),
    )