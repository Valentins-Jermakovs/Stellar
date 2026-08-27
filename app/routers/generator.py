from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.facades import CVGeneratorFacade
from app.schemas import CVGenerateRequest

from .dependencies import (
    get_generator_facade,
    jwt_auth,
)


router = APIRouter(
    prefix="/cvs",
    tags=["CV Generator"],
)


@router.post(
    "/{cv_id}/generate",
)
async def generate_cv(
    cv_id: int,
    data: CVGenerateRequest,
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: CVGeneratorFacade = Depends(
        get_generator_facade
    ),
):
    return Response(
        content=await facade.generate(
            cv_id=cv_id,
            user_id=int(current_user["sub"]),
            template=data.template,
        ),
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="cv-{cv_id}.pdf"'
            )
        },
    )