import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()

class AppSettings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    MODEL_CONFIG = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL_TEST: str = "sqlite+aiosqlite:///:memory:"

settings = AppSettings()