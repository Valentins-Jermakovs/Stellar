import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    MERIDIAN_URL: str = os.getenv(
        "MERIDIAN_URL",
        "http://localhost:8000",
    )


settings = Settings()