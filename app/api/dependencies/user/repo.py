from app.core.clients.db import get_async_session
from app.core.log.loguru_logger_repository import get_logger_repo
from app.core.log.logger_repository import LoggerRepository
from app.modules.user.infraestructure.repositories.sqlmodel_user_repository import PostgresUserRepository
from app.modules.user.domain.repository_user import UserRepository

from fastapi import Depends

def get_user_repo(db = Depends(get_async_session, scope="function"), logger: LoggerRepository = Depends(get_logger_repo)) -> UserRepository:
    return PostgresUserRepository(db, logger)