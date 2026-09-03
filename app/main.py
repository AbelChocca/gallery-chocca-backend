# Principal depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from redis.asyncio import from_url

# App depends
from app.core.log.config import logger_service
from app.api.middlewares.manager import init_middlewares
from app.infra.db.config import init_db
from app.core.settings.pydantic_settings import settings
from app.infra.storage.config import init_cloudinary_client

from app.features.user import user_route
from app.features.slides import slide_route
from app.features.products import product_route
from app.features.favorites import favorites_router
from app.features.dashboard import dashboard_route
from app.features.inventory import inventory_route
from app.features.auth import auth_route
from app.features.cart import cart_route
from app.features.material import material_route
from app.features.reports import reports_route
from app.features.balancing.routes.balance_snapshots import balance_snapshot_router
from app.features.balancing.routes.other_current_liability import other_current_liability_router
from app.features.balancing.routes.inventory_valuation import inventory_valuation_router
from app.features.balancing.routes.accounts_receivables import account_receivable_router
from app.features.balancing.routes.accounts_payables import account_payable_router
from app.features.balancing.routes.financial_debts import financial_debt_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger_service.info('🚀 Iniciandoo App')
    try:
        await init_db()
        redis = from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )

        await redis.ping()

        app.state.redis = redis

        logger_service.info("✅ Base de datos inicializada correctamente.")

        init_cloudinary_client()

        logger_service.info("✅ Storage inicializada correctamente.")

        try:
            redis_connected = await redis.ping()
            if not redis_connected:
                logger_service.warning('⚠️ No se pudo verificar la conexión con el cliente Redis')
                raise RuntimeError('❌ Error de conexion con Redis.')
        finally:
            logger_service.info("✅ Redis service was inicializated correctly")

    except Exception as e:
        logger_service.error(f'Error al inicializar los servicios: {e}')
        raise 

    yield

    await redis.close()

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
app.include_router(auth_route.router)
app.include_router(favorites_router.router)
app.include_router(dashboard_route.router)
app.include_router(inventory_route.router)
app.include_router(cart_route.router)
app.include_router(material_route.router)
app.include_router(reports_route.router)
app.include_router(balance_snapshot_router.balance_router)
app.include_router(account_payable_router.accounts_payable_router)
app.include_router(account_receivable_router.accounts_receivable_router)
app.include_router(inventory_valuation_router.inventory_valuation_router)
app.include_router(financial_debt_router.financial_debt_router)
app.include_router(other_current_liability_router.other_current_liability_router)