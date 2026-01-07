from app.domain.user.entity import User
from app.infra.db.models.model_user import UserTable

from app.infra.db.mappers.base_mapper import BaseMapper

from typing import Optional

class UserMapper:
    @staticmethod
    def to_entity(model: UserTable) -> User:
        return User(
            id=model.id,
            name=model.nombre,
            email=model.email,
            role=model.role,
            hashed_password=model.hashed_password
        )
    
    @staticmethod
    def to_db_model(user: User, user_db: Optional[UserTable] = None) -> UserTable:
        if user_db:
            user_db.nombre = user_db.nombre
            user_db.email = user.email
            user_db.role = user.role
            user_db.hashed_password = user.hashed_password
            return user_db
        return UserTable(
            nombre=user.name,
            email=user.email,
            role=user.role,
            hashed_password=user.hashed_password
        )