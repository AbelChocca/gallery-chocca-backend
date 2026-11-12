from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import NullPool
from app.core.settings.pydantic_test_settings import test_settings

engine = create_async_engine(
    test_settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    poolclass=NullPool
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)