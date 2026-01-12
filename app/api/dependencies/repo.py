from app.infra.db.factory_repository import FactoryRespository
from app.infra.db.config import get_async_session

from app.core.log.protocole import LoggerProtocol
from app.core.log.loguru_service import get_logger_service

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession


def get_fatory_repo(
        db_session: AsyncSession = Depends(get_async_session, scope="function"),
        logger: LoggerProtocol = Depends(get_logger_service)
        ) -> FactoryRespository:
    return FactoryRespository(
        db_session=db_session,
        logger=logger
    )