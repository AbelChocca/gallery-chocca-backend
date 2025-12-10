from app.core.clients.db import get_async_session
from app.core.log.logger_repository_loguru import get_logger_repo
from app.core.log.repository_logger import LoggerRepository
from app.modules.user.infra.repositories.infra_user_repo import PostgresUserRepository
from app.modules.user.domain.repository_user import UserRepository

from fastapi import Depends

def get_user_repo(db = Depends(get_async_session, scope="function"), logger: LoggerRepository = Depends(get_logger_repo)) -> UserRepository:
    return PostgresUserRepository(db, logger)