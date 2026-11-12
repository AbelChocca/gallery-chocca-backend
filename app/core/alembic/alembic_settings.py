from pydantic_settings import BaseSettings, SettingsConfigDict


class AlembicSettings(BaseSettings):
    ENV: str

    DATABASE_URL: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_HOST: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_PORT: int = 5432

    model_config = SettingsConfigDict(extra="ignore")


alembic_settings = AlembicSettings()