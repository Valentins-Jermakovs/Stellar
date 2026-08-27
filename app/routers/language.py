from fastapi import APIRouter, Depends, status

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

from .dependencies import (
    get_cv_language_facade,
    get_language_facade,
    jwt_auth,
)


router = APIRouter(
    tags=["Languages"],
)


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
    return await facade.create(data)


@router.get(
    "/languages",
    response_model=list[LanguageRead],
)
async def get_languages(
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: LanguageFacade = Depends(
        get_language_facade
    ),
):
    return await facade.get_all()


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
    return await facade.get_by_id(
        language_id
    )


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
    return await facade.add(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        data=data,
    )


@router.get(
    "/cvs/{cv_id}/languages",
    response_model=list[CVLanguageRead],
)
async def get_cv_languages(
    cv_id: int,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVLanguageFacade = Depends(
        get_cv_language_facade
    ),
):
    return await facade.get_by_cv_id(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
    )


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
    return await facade.update(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        language_id=language_id,
        data=data,
    )


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
    await facade.delete(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        language_id=language_id,
    )