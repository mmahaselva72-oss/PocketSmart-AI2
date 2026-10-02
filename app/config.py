import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "change-this-in-production"
    )

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./pocketsmart.db"
    )


settings = Settings()

# Backward-compatible variables used by the existing project files
GEMINI_API_KEY = settings.GEMINI_API_KEY
SECRET_KEY = settings.SECRET_KEY
DATABASE_URL = settings.DATABASE_URL