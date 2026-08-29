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

from app.facades import (
    CVLanguageFacade,
    LanguageFacade,
)

from app.schemas import (
    CVLanguageCreate,
    CVLanguageRead,
    CVLanguageUpdate,
    LanguageCreate,
    LanguageRead,
)


# ==============================
# Router dependencies
# ==============================

from .dependencies import (
    get_cv_language_facade,
    get_language_facade,
    jwt_auth,
)


# ==============================
# Language router
# ==============================

router = APIRouter(
    tags=["Languages"],
)


# Create a new language in the global catalog.
@router.post(
    "/languages",
    response_model=LanguageRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_language(
    data: LanguageCreate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: LanguageFacade = Depends(
        get_language_facade
    ),
):
    """
    Create a new global language.

    The language is stored in the shared language catalog
    and can later be associated with CVs.
    """

    return await facade.create(
        data
    )


# Search languages in the global catalog.
@router.get(
    "/languages",
    response_model=list[LanguageRead],
)
async def search_languages(
    query: str | None = Query(
        default=None,
        description="Search languages by name",
    ),
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: LanguageFacade = Depends(
        get_language_facade
    ),
):
    """
    Search the global language catalog.

    The optional query is used to find languages
    whose names match the specified search term.
    """

    return await facade.search(
        query=query
    )


# Return a language from the global catalog by ID.
@router.get(
    "/languages/{language_id}",
    response_model=LanguageRead,
)
async def get_language(
    language_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: LanguageFacade = Depends(
        get_language_facade
    ),
):
    """
    Return a global language by ID.

    The language ID is passed to the facade
    to retrieve the corresponding catalog entry.
    """

    return await facade.get_by_id(
        language_id
    )


# Add a language from the global catalog to a CV.
@router.post(
    "/cvs/{cv_id}/languages",
    response_model=CVLanguageRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_language_to_cv(
    cv_id: int,
    data: CVLanguageCreate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVLanguageFacade = Depends(
        get_cv_language_facade
    ),
):
    """
    Add a language to a CV.

    The authenticated user's ID is passed to the facade
    to verify ownership of the specified CV.
    """

    return await facade.add(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


# Update a language association in a CV.
@router.patch(
    "/cvs/{cv_id}/languages/{language_id}",
    response_model=CVLanguageRead,
)
async def update_cv_language(
    cv_id: int,
    language_id: int,
    data: CVLanguageUpdate,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVLanguageFacade = Depends(
        get_cv_language_facade
    ),
):
    """
    Update a language association in a CV.

    The authenticated user's ID is passed to the facade
    to verify ownership of the specified CV.
    """

    return await facade.update(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        language_id=language_id,
        data=data,
    )


# Delete a language association from a CV.
@router.delete(
    "/cvs/{cv_id}/languages/{language_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_cv_language(
    cv_id: int,
    language_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVLanguageFacade = Depends(
        get_cv_language_facade
    ),
):
    """
    Delete a language association from a CV.

    The authenticated user's ID is passed to the facade
    to verify ownership of the specified CV.
    """

    await facade.delete(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        language_id=language_id,
    )