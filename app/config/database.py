# ==============================
# Library imports
# ==============================

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from sqlmodel import SQLModel


# ==============================
# Application imports
# ==============================

# Import all application models so they are registered in
# SQLModel metadata before database tables are created.
from app import models

from .settings import settings


# ==============================
# Database configuration
# ==============================

# PostgreSQL connection URL built from application settings.
DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)


# ==============================
# Database engine
# ==============================

# Create the asynchronous database engine.
#
# echo=True enables SQL query logging.
# pool_pre_ping=True checks connections before using them.
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)


# ==============================
# Database session
# ==============================

# Create a factory for asynchronous database sessions.
#
# expire_on_commit=False keeps loaded objects available after
# a commit instead of expiring their attributes.
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ==============================
# Database dependencies
# ==============================

async def get_session():
    """
    Provide an asynchronous database session for FastAPI dependencies.
    """

    async with async_session() as session:
        yield session


# ==============================
# Database initialization
# ==============================

async def init_db() -> None:
    """
    Create all database tables defined in SQLModel metadata.
    """

    async with engine.begin() as connection:
        await connection.run_sync(
            SQLModel.metadata.create_all
        )