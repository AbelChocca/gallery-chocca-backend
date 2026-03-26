from loguru import logger
import sys
from contextvars import ContextVar

from app.core.settings.pydantic_settings import settings
from app.core.log.json_sink import json_sink

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

        def add_request_id(record):
            record["extra"]["request_id"] = request_id_var.get("-")

        logger.configure(
            patcher=add_request_id
        )
        logger.add(
            lambda m: json_sink(m, sys.stdout),
            level=settings.LOG_LEVEL,
            filter=lambda r: r["level"].no < 40,
        )
        logger.add(
            lambda m: json_sink(m, sys.stderr),
            level="ERROR",
        )

        self._logger = logger
    
logger_service = LoggerSingleton()._logger
