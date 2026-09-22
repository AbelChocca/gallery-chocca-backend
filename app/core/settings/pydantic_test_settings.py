from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    PYTHONPATH: str
    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432

    # Configuración del settings
    model_config = SettingsConfigDict(
        env_file=".env.test",
        extra="ignore",
    )

test_settings = Settings()