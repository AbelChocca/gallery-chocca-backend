from loguru import logger
import sys
from pathlib import Path
from contextvars import ContextVar

from app.core.settings.pydantic_settings import settings

request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)

class LoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance._configure()
        return cls._instance

    def _configure(self):
        logger.remove()  # limpiamos handlers por defecto

        # Sinks: consola + archivo rotativo
        logger.add(
            sys.stderr,
            level=settings.LOG_LEVEL,
            format=settings.LOG_FORMAT,
            backtrace=True,
            diagnose=False,
        )

        logs_dir = Path(settings.LOG_PATH)
        logs_dir.mkdir(exist_ok=True)

        logger.add(
            logs_dir / "app.log",
            rotation="10 MB",
            compression="zip",
            level=settings.LOG_LEVEL,
            format=settings.LOG_FORMAT,
            backtrace=True,
            diagnose=False,
        )

        self._logger = logger

    def get_logger(self):
        request_id = request_id_var.get("-")
        return self._logger.bind(request_id=request_id)
    
logger_service = LoggerSingleton().get_logger()
