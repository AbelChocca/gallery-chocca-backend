from app.infra.db.repositories.sqlmodel_product_repository import PostgresProductRepository
from app.infra.db.factory_repository import FactoryRespository
from app.api.dependencies.repo import get_fatory_repo

from fastapi import Depends

def get_product_repo(
        factory: FactoryRespository = Depends(get_fatory_repo)
    ) -> PostgresProductRepository:
    return factory.get_product_repository()