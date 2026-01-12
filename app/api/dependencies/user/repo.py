from app.infra.db.factory_repository import FactoryRespository
from app.infra.db.repositories.sqlmodel_user_repository import PostgresUserRepository
from app.api.dependencies.repo import get_fatory_repo

from fastapi import Depends

def get_user_repo(factory: FactoryRespository = Depends(get_fatory_repo)) -> PostgresUserRepository:
    return factory.get_user_repository()