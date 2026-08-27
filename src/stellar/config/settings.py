import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    # ============================================================
    # MERIDIAN
    # ============================================================

    MERIDIAN_URL: str = os.getenv(
        "MERIDIAN_URL",
        "http://localhost:8000",
    )


    # ============================================================
    # FLASK
    # ============================================================

    FLASK_SECRET_KEY: str = os.getenv(
        "FLASK_SECRET_KEY",
        "change-me",
    )


    # ============================================================
    # POSTGRESQL
    # ============================================================

    POSTGRES_HOST: str = os.getenv(
        "POSTGRES_HOST",
        "localhost",
    )

    POSTGRES_PORT: int = int(
        os.getenv(
            "POSTGRES_PORT",
            "5432",
        )
    )

    POSTGRES_DB: str = os.getenv(
        "POSTGRES_DB",
        "stellar",
    )

    POSTGRES_USER: str = os.getenv(
        "POSTGRES_USER",
        "stellar",
    )

    POSTGRES_PASSWORD: str = os.getenv(
        "POSTGRES_PASSWORD",
        "stellar",
    )


settings = Settings()