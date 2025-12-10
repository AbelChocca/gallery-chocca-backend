from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.engine import create_async_engine, AsyncEngine
from app.core.settings.pydantic_settings import settings
from typing import AsyncGenerator

DATABASE_URL = settings.DATABASE_URL

engine: AsyncEngine = create_async_engine(url=DATABASE_URL, echo=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Funcion para proveer una session asincronica a la base de datos.
    """
    async with AsyncSession(engine) as session:
        yield session

async def init_db():
    """
    Funcion para inicializar la base de datos de manera asincronica
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)