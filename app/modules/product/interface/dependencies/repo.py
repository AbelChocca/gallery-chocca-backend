from app.core.clients.db import get_async_session
from app.core.log.repository_logger import LoggerRepository
from app.core.log.logger_repository_loguru import get_logger_repo
from app.modules.product.domain.repositories.repository_product import ProductRepository
from app.modules.product.infra.repositories.infra_product_repository import PostgresProductRepository

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession


def get_product_repo(
        db: AsyncSession = Depends(get_async_session, scope="function"), 
        logger: LoggerRepository = Depends(get_logger_repo)
        ) -> ProductRepository:
    return PostgresProductRepository(db, logger)