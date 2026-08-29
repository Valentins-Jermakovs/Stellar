# ==============================
# Library imports
# ==============================

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


# ==============================
# Application settings
# ==============================

class Settings(BaseSettings):
    """
    This class represents the application settings.

    It uses Pydantic's `BaseSettings` to load and validate
    configuration values from environment variables and the `.env` file.
    """

    # PostgreSQL connection settings.
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # Redis connection settings.
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str | None = None

    # JWT token settings.
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    # .env file configuration.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Create an instance of the settings class.
settings = Settings()