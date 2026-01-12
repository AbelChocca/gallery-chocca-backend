from app.infra.db.factory_repository import FactoryRespository
from app.infra.db.repositories.sqlmodel_slide_repository import PostgresSlideRepository
from app.api.dependencies.repo import get_fatory_repo

from fastapi import Depends

def get_slide_repo(factory: FactoryRespository = Depends(get_fatory_repo)) -> PostgresSlideRepository:
    return factory.get_slide_repository()