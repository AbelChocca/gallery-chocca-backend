# Principal depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# App depends
from app.core.log.config import logger_service
from app.api.middlewares.manager import init_middlewares
from app.infra.db.config import init_db
from app.infra.media.config import init_cloudinary_client
from app.infra.cache.config import get_redis_client
from app.core.settings.pydantic_settings import settings

from app.api.v1.user import user_route
from app.api.v1.slides import slide_route
from app.api.v1.media import media_router
from app.api.v1.products import product_route
from app.api.v1.favorites import favorites_router
from app.api.v1.dashboard import dashboard_route
from app.api.v1.inventory import inventory_route

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger_service.info('🚀 Iniciandoo App')
    try:
        await init_db()
        init_cloudinary_client()

        logger_service.info("✅ Base de datos inicializada correctamente.")

        try:
            redis_connected = await get_redis_client().ping()
            if not redis_connected:
                logger_service.warning('⚠️ No se pudo verificar la conexión con el cliente Redis')
                raise RuntimeError('❌ Error de conexion con Redis.')
        finally:
            logger_service.info(f"✅ Redis service was inicializated correctly")

    except Exception as e:
        logger_service.error(f'Error al inicializar los servicios: {e}')
        raise 

    yield

    logger_service.info("🛑 Cerrando aplicación y liberando recursos...")

is_prod = settings.ENV == "production"

app = FastAPI(
    title='Galeria Chocca', 
    lifespan=lifespan, 
    docs_url=None if is_prod else '/docs',
    redoc_url=None if is_prod else '/redoc',
    openapi_url=None if is_prod else '/openapi.json'
)
init_middlewares(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.ALLOW_ORIGINS,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

app.include_router(user_route.router)
app.include_router(product_route.router)
app.include_router(slide_route.router)
app.include_router(media_router.router)
app.include_router(favorites_router.router)
app.include_router(dashboard_route.router)
app.include_router(inventory_route.router)