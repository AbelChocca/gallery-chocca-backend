from app.domain.media.protocol import MediaProtocol
from app.infra.media.cloudinary_service import CloudinaryService
from app.core.log.protocole import LoggerProtocol
from app.core.log.loguru_service import get_logger_service

from fastapi import Depends

def get_media_service(
        logger: LoggerProtocol = Depends(get_logger_service)
        ) -> MediaProtocol:
    return CloudinaryService(logger)