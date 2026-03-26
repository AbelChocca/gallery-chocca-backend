from app.core.log.protocole import LoggerProtocol
from app.core.log.config import logger_service
from functools import lru_cache

class LoguruLoggerService(LoggerProtocol):
    def __init__(self, logger):
        self.logger_service = logger

    def info(self, message: str, **kwargs) -> None:
        if kwargs:
            self.logger_service.bind(**kwargs).info(message)
        else:
            self.logger_service.info(message)

    def warning(self, message: str, **kwargs) -> None:
        if kwargs:
            self.logger_service.bind(**kwargs).warning(message)
        else:
            self.logger_service.warning(message)

    def error(self, message: str, **kwargs) -> None:
        if kwargs:
            self.logger_service.bind(**kwargs).error(message)
        else:
            self.logger_service.error(message)

    def debug(self, message: str, **kwargs) -> None:
        if kwargs:
            self.logger_service.bind(**kwargs).debug(message)
        else:
            self.logger_service.debug(message)

    def exception(self, message: str, **kwargs) -> None:
        if kwargs:
            self.logger_service.bind(**kwargs).exception(message)
        else:
            self.logger_service.exception(message)

@lru_cache
def get_logger_service() -> LoggerProtocol:
    return LoguruLoggerService(logger_service)