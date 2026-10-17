# ==============================
# Library Imports
# ==============================

from contextlib import asynccontextmanager

from fastapi import FastAPI


# ==============================
# Application Imports
# ==============================

from app.config.database import (
    engine,
    init_db,
)

from app.config.redis import (
    close_redis,
    init_redis,
)

from app.routers import main_router


# ==============================
# Application Lifecycle
# ==============================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage database and Redis connections during application startup
    and shutdown.
    """

    try:
        # Initialize PostgreSQL and Redis.
        await init_db()
        await init_redis()

        yield

    finally:
        # Close Redis and release database connections.
        try:
            await close_redis()
        finally:
            await engine.dispose()


# ==============================
# FastAPI Application
# ==============================

app = FastAPI(
    title="Stellar",
    lifespan=lifespan,
)


# ==============================
# Router Registration
# ==============================

app.include_router(
    main_router,
)