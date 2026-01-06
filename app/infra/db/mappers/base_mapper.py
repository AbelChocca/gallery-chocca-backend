from app.infra.db.types import E, M
from typing import Generic, Optional
from abc import ABC, abstractmethod

class BaseMapper(Generic[E, M], ABC):
    @staticmethod
    @abstractmethod
    def to_db_model(entity: E, existing_model: Optional[M] = None) -> M:
        ...

    @staticmethod
    @abstractmethod
    def to_entity(model: M) -> E:
        ...