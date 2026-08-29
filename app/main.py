# ==============================
# Library imports
# ==============================

from contextlib import asynccontextmanager

from fastapi import FastAPI


# ==============================
# Database initialization
# ==============================

from app.config.database import init_db
from app.config.redis import (
    init_redis,
    close_redis,
)


# ==============================
# Router imports
# ==============================

from app.routers import main_router


# ==============================
# Application lifecycle
# ==============================

@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    """
    Manage the FastAPI application lifecycle.

    Initialize the PostgreSQL database and Redis connection
    when the application starts, and close the Redis connection
    when the application shuts down.
    """

    # Initialize PostgreSQL.
    await init_db()

    # Initialize Redis.
    await init_redis()

    yield

    # Close the Redis connection.
    await close_redis()


# ==============================
# FastAPI application
# ==============================

app = FastAPI(
    lifespan=lifespan,
)


# ==============================
# Router registration
# ==============================

app.include_router(
    main_router,
)