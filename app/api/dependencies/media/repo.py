from app.infra.db.repositories.sqlmodel_image_repository import PostgresImageRepository
from app.infra.db.factory_repository import FactoryRespository

from app.api.dependencies.repo import get_fatory_repo

from fastapi import Depends

def get_image_repo(factory: FactoryRespository = Depends(get_fatory_repo)) -> PostgresImageRepository:
    return factory.get_image_repository()
