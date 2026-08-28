from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Pydantic validates the values according to the types defined below,
    so, for example, POSTGRES_PORT and REDIS_PORT are converted to integers.
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

    # Redis password is optional because authentication may be disabled.
    REDIS_PASSWORD: str | None = None

    # Secret key used to sign JWT tokens.
    JWT_SECRET_KEY: str

    # Algorithm used to sign and verify JWT tokens.
    JWT_ALGORITHM: str

    # Settings configuration.
    model_config = SettingsConfigDict(
        # Load additional values from the `.env` file when running locally.
        env_file=".env",

        # Read the `.env` file using UTF-8 encoding.
        env_file_encoding="utf-8",

        # Ignore environment variables that are not defined in this class.
        extra="ignore",
    )


# Create one settings instance for the whole application.
# Other modules can import this object and use the same configuration.
settings = Settings()
