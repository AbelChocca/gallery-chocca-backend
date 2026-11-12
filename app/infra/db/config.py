from sqlmodel import SQLModel
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from app.core.settings.pydantic_settings import settings

from app.infra.db import model_registry  # noqa: F401

def get_db_url() -> URL:
    if settings.DATABASE_URL:
        url = make_url(settings.DATABASE_URL)

        if not url.drivername.startswith("postgresql"):
            raise ValueError("DATABASE_URL debe utilizar PostgreSQL")

        return url.set(
            drivername="postgresql+asyncpg",
        ).difference_update_query(
            ["sslmode", "ssl"]
        )

    if not all((
        settings.POSTGRES_USER,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST,
        settings.POSTGRES_DB,
    )):
        raise ValueError(
            "Configura DATABASE_URL o las variables POSTGRES_*"
        )

    return URL.create(
        drivername="postgresql+asyncpg",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
    )

engine: AsyncEngine = create_async_engine(
    get_db_url(),
    echo=False,
    pool_size=3,
    max_overflow=2,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_timeout=30,
    connect_args=(
        {"ssl": "require"}
        if settings.ENV == "production"
        else {}
    ),
)

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