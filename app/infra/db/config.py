from sqlmodel import SQLModel
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from app.core.settings.pydantic_settings import settings

def get_db_url():
    ssl_mode = {}

    if settings.ENV == "prod":
        ssl_mode = {"ssl": "require"}

    return URL.create(
        drivername="postgresql+asyncpg",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=5432,
        database=settings.POSTGRES_DB,
        query=ssl_mode
    )


engine: AsyncEngine = create_async_engine(get_db_url(), echo=False, pool_size=10, max_overflow=5)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def init_db():
    """
    Funcion para inicializar la base de datos de manera asincronica
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)