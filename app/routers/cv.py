from fastapi import APIRouter, Depends, Query, status

from app.facades import CVFacade

from app.schemas import (
    CVCreate,
    CVDetailRead,
    CVPageRead,
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


# ==========================================
# Create
# ==========================================

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


# ==========================================
# Search / List
# ==========================================

@router.get(
    "",
    response_model=CVPageRead,
)
async def search_cvs(
    query: str | None = Query(
        default=None,
        description="Search CVs by title",
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVFacade = Depends(
        get_cv_facade
    ),
):
    return await facade.search(
        user_id=int(current_user["sub"]),
        query=query,
        page=page,
        page_size=page_size,
    )


# ==========================================
# Get Detail
# ==========================================

@router.get(
    "/{cv_id}",
    response_model=CVDetailRead,
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


# ==========================================
# Update
# ==========================================

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


# ==========================================
# Delete
# ==========================================

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