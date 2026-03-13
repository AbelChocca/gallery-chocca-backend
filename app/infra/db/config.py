from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from app.core.settings.pydantic_settings import settings

DATABASE_URL = settings.DATABASE_URL

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)

async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False
)

async def init_db():
    """
    Funcion para inicializar la base de datos de manera asincronica
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)