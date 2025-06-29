import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class AppSettings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    MODEL_CONFIG = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL_TEST: str = "sqlite+aiosqlite:///:memory:"


settings = AppSettings()
