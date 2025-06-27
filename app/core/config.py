from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    # A URL para asyncpg usa 'postgresql+asyncpg://'
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/your_database_name"
    # Certifique-se de substituir 'user', 'password' e 'your_database_name'
    # por suas credenciais reais do PostgreSQL.

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = AppSettings()