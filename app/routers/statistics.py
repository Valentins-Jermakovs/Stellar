# ==============================
# Library imports
# ==============================

from fastapi import (
    APIRouter,
    Depends,
)


# ==============================
# Application imports
# ==============================

from app.facades import StatisticsFacade

from app.schemas import CVStatistics


# ==============================
# Router dependencies
# ==============================

from .dependencies import (
    get_statistics_facade,
    jwt_auth,
)


# ==============================
# Statistics router
# ==============================

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
)


# Return statistics for the current user.
@router.get(
    "",
    response_model=CVStatistics,
)
async def get_statistics(
    current_user: dict = Depends(
        jwt_auth.get_current_user
    ),
    facade: StatisticsFacade = Depends(
        get_statistics_facade
    ),
) -> CVStatistics:
    """
    Return statistics for the current user.
    """

    return await facade.get_user_statistics(
        user_id=int(current_user["sub"]),
    )