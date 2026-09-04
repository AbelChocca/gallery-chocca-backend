from pydantic_settings import BaseSettings, SettingsConfigDict


class AlembicSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    ENV: str

    model_config = SettingsConfigDict(extra="ignore")


alembic_settings = AlembicSettings()