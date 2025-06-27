import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()

class AppSettings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = AppSettings()