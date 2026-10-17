
# ==============================
# Library Imports
# ==============================

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy import text


# ==============================
# Application Imports
# ==============================

from app.config.database import engine
from app.config.redis import get_redis
from app.routers.dependencies import jwt_auth


# ==============================
# Health Router
# ==============================

router = APIRouter(
    tags=["Health"],
)


# ==============================
# API Health Check
# ==============================

@router.get("/health")
async def health_check(
    admin: dict = Depends(
        jwt_auth.require_roles(["admin"])
    ),
) -> dict[str, str]:
    """Return the API health status for administrators."""

    return {
        "status": "ok",
    }


# ==============================
# Application Readiness Check
# ==============================

@router.get("/health/ready")
async def readiness_check(
    admin: dict = Depends(
        jwt_auth.require_roles(["admin"])
    ),
) -> dict[str, str]:
    """Check whether PostgreSQL and Redis are available."""

    # Check PostgreSQL.
    try:
        async with engine.connect() as connection:
            await connection.execute(
                text("SELECT 1")
            )
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database is unavailable.",
        ) from None

    # Check Redis.
    try:
        redis = await get_redis()
        await redis.ping()
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable.",
        ) from None

    return {
        "status": "ready",
        "database": "ok",
        "redis": "ok",
    }
