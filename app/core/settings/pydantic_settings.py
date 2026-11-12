import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str
    TOKEN_ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_SECONDS: int
    REFRESH_TOKEN_EXPIRES_SECONDS: int

    COOKIE_DOMAIN: str

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
    DATABASE_URL: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_HOST: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_PORT: int = 5432

    # google captcha
    RECAPTCHA_SECRET_KEY: str

    ENV: str

    OPENPAY_MERCHANT_ID: str | None = None
    OPENPAY_PRIVATE_KEY: str | None = None
    OPENPAY_BASE_URL: str | None = None
    OPENPAY_TEST_CLIENT_IP: str | None = None

    FRONTEND_URL: str

    FACTUSMART_BASE_URL: str | None = None
    FACTUSMART_API_KEY: str | None = None
    FACTUSMART_RUC: str | None = None

    RESEND_API_KEY: str
    RESEND_FROM_EMAIL: str

    RESEND_COMPLAINTS_FROM_EMAIL: str

    RESEND_ORDERS_FROM_EMAIL: str

    RESEND_SUPPORT_FROM_EMAIL: str

    COMPLAINT_REPLY_TO_EMAIL: str

    COMPLAINT_PROVIDER_LEGAL_NAME: str
    COMPLAINT_PROVIDER_RUC: str
    COMPLAINT_PROVIDER_ADDRESS: str

    # Configuración del settings
    model_config = SettingsConfigDict(
        env_file=(
            ".env.test"
            if os.getenv("ENV") == "test"
            else ".env"
        ),
        extra="ignore",
    )

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()