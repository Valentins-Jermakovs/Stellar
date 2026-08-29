# ==============================
# Library imports
# ==============================

from fastapi import (
    APIRouter,
    Depends,
)

from fastapi.responses import Response


# ==============================
# Application imports
# ==============================

from app.facades import CVGeneratorFacade

from app.schemas import CVGenerateRequest

from .dependencies import (
    get_generator_facade,
    jwt_auth,
)


# ==============================
# Router configuration
# ==============================

router = APIRouter(
    prefix="/cvs",
    tags=["CV Generator"],
)


# ==============================
# Generate CV
# ==============================

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
    """
    Generate a PDF document from the specified CV.

    The authenticated user's ID is passed to the facade
    to verify ownership of the CV before generating the document.
    The selected template and language are taken from the request data.
    """
    pdf = await facade.generate(
        cv_id=cv_id,
        user_id=int(current_user["sub"]),
        template=data.template,
        language=data.language,
    )

    # Return the generated PDF as a downloadable response.
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="cv-{cv_id}.pdf"'
            )
        },
    )