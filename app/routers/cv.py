# ==============================
# Library imports
# ==============================

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)


# ==============================
# Application imports
# ==============================

from app.facades import CVFacade

from app.schemas import (
    CVCreate,
    CVDetailRead,
    CVPageRead,
    CVRead,
    CVUpdate,
)


# ==============================
# Router dependencies
# ==============================

from .dependencies import (
    get_cv_facade,
    jwt_auth,
)


# ==============================
# CV router
# ==============================

router = APIRouter(
    prefix="/cvs",
    tags=["CV"],
)


# Create a new CV.
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
    """
    Create a new CV.
    """

    return await facade.create(
        user_id=int(current_user["sub"]),
        data=data,
    )


# Search the current user's CVs with pagination.
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
    """
    Return a paginated list of the current user's CVs.
    """

    return await facade.search(
        user_id=int(current_user["sub"]),
        query=query,
        page=page,
        page_size=page_size,
    )


# Return a CV by its ID.
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
    """
    Return a CV by ID.
    """

    return await facade.get_by_id(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
    )


# Update an existing CV.
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
    """
    Update an existing CV.
    """

    return await facade.update(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


# Delete an existing CV.
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
    """
    Delete an existing CV.
    """

    await facade.delete(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
    )