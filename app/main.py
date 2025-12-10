# Principal depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator

# App depends
from app.core.log.config import logger_service
from app.core.middlewares.manager import init_middlewares
from app.core.clients.db import init_db
from app.core.clients.cloudinary import init_cloudinary_client
from app.core.clients.redis_client import get_redis_client
from app.core.settings.pydantic_settings import settings

from app.modules.product.interface import product_route
from app.modules.user.interface import user_route
from app.modules.slide.interface import slide_route
from app.modules.cloudinary.interface import cloudinary_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger_service.info('🚀 Iniciandoo App')
    try:
        await init_db()
        init_cloudinary_client()

        logger_service.info("✅ Base de datos inicializada correctamente.")

        redis_connected = await get_redis_client().ping()
        if not redis_connected:
            logger_service.warning('⚠️ No se pudo verificar la conexión con el cliente Redis')
            raise RuntimeError('❌ Error de conexion con Redis.')

    except Exception as e:
        logger_service.error(f'Error al inicializar los servicios: {e}')
        raise 

    yield

    logger_service.info("🛑 Cerrando aplicación y liberando recursos...")

app = FastAPI(title='Galeria Chocca', lifespan=lifespan)
init_middlewares(app)
Instrumentator().instrument(app).expose(app=app)

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
app.include_router(cloudinary_router.router)