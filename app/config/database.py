# SQLAlchemy provides the async engine and session tools used
# to work with PostgreSQL without blocking the event loop.
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from sqlmodel import SQLModel

# Import all application models so they are registered in
# SQLModel.metadata before the database tables are created.
from app import models

from .settings import settings


# PostgreSQL connection URL built from application settings.
DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)


# Create the asynchronous database engine.
#
# echo=True enables SQL query logging.
# pool_pre_ping=True checks connections before using.
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)


# Factory used to create asynchronous database sessions.
#
# expire_on_commit=False keeps loaded objects available after a commit
# instead of expiring their attributes.
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    """Provide a database session for FastAPI dependencies."""
    async with async_session() as session:
        yield session


async def init_db() -> None:
    """Create all database tables defined in SQLModel metadata."""
    async with engine.begin() as connection:
        await connection.run_sync(
            SQLModel.metadata.create_all
        )

