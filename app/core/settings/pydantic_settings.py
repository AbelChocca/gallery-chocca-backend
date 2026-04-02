from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # PostgreSQL
    DATABASE_URL: str
    # JWT
    SECRET_KEY: str
    TOKEN_ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_SECONDS: int
    REFRESH_TOKEN_EXPIRES_SECONDS: int

    # Cloudinary
    CLOUDINARY_NAME: str
    CLOUDINARY_API_SECRET: str
    CLOUDINARY_API_KEY: str

    # Cors
    ALLOW_ORIGINS: list[str]

    # REDIS
    REDIS_URL: str

    # REDIS TTL
    REDIS_LARGE_TTL: int
    REDIS_MEDIUM_TTL: int
    REDIS_SHORT_TTL: int
    REDIS_MIN_TTL: int

    # base de datos que usaremos en producción
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # google captcha
    RECAPTCHA_SECRET_KEY: str

    ENV: str

    # Configuración del settings
    model_config = SettingsConfigDict(env_file='.env')

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()