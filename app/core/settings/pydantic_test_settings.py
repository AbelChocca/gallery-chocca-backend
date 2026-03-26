from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    PYTHONPATH: str
    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Configuración del settings
    model_config = SettingsConfigDict(env_file='.env.test')

test_settings = Settings()