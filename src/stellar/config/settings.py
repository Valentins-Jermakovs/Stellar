import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    MERIDIAN_URL: str = os.getenv(
        "MERIDIAN_URL",
        "http://localhost:8000",
    )

    FLASK_SECRET_KEY: str = os.getenv(
        "FLASK_SECRET_KEY",
        "change-me",
    )


settings = Settings()