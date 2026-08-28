from fastapi import APIRouter, Depends

from app.facades import StatisticsFacade
from app.schemas import CVStatistics

from .dependencies import (
    get_statistics_facade,
    jwt_auth,
)


router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
)


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
    """Return statistics for the current user."""
    return await facade.get_user_statistics(
        user_id=int(current_user["sub"]),
    )