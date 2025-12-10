from app.modules.slide.domain.slide_repository import SlideRepository
from app.modules.slide.infra.slide_infra_repository import InfraSlideRepository
from app.core.log.repository_logger import LoggerRepository
from app.core.clients.db import get_async_session
from app.core.log.logger_repository_loguru import get_logger_repo

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

def get_slide_repo(db_sesison: AsyncSession = Depends(get_async_session, scope="function"), logger: LoggerRepository = Depends(get_logger_repo)) -> SlideRepository:
    return InfraSlideRepository(db_sesison, logger)