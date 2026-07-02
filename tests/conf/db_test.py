from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import NullPool
from app.core.settings.pydantic_test_settings import test_settings

engine = create_async_engine(
    test_settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    poolclass=NullPool
)