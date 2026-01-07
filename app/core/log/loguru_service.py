from app.core.log.protocole import LoggerProtocol
from app.core.log.config import logger_service
from functools import lru_cache
from loguru import Logger

class LoguruLoggerService(LoggerProtocol):
    def __init__(self, logger: Logger):
        self.logger_service: Logger = logger

    def info(self, message: str, **kwargs) -> None:
        self.logger_service.info(message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        self.logger_service.warning(message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self.logger_service.error(message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        self.logger_service.debug(message, **kwargs)

@lru_cache
def get_logger_repo() -> LoggerProtocol:
    return LoguruLoggerService(logger_service)