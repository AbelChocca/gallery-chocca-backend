from app.core.log.repository_logger import LoggerRepository
from app.core.log.config import logger_service
from functools import lru_cache

class LoguruLoggerRepository(LoggerRepository):
    def __init__(self, logger):
        self.logger_service = logger

    def info(self, message: str, **kwargs) -> None:
        self.logger_service.info(message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        self.logger_service.warning(message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self.logger_service.error(message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        self.logger_service.debug(message, **kwargs)

@lru_cache
def get_logger_repo() -> LoggerRepository:
    return LoguruLoggerRepository(logger_service)