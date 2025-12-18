from app.modules.cloudinary.domain.cloudinary_repository import CloudinaryRepository
from app.modules.cloudinary.infra.infra_cloudinary_repository import InfraCloudinaryRepository
from app.core.log.logger_repository import LoggerRepository
from app.core.log.loguru_logger_repository import get_logger_repo

from fastapi import Depends

def get_cloudinary_repo(logger: LoggerRepository = Depends(get_logger_repo)) -> CloudinaryRepository:
    return InfraCloudinaryRepository(logger)