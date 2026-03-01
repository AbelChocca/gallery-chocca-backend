from app.domain.user.entity import User
from app.infra.db.models.model_user import UserTable

from app.infra.db.mappers.base_mapper import BaseMapper

class UserMapper(BaseMapper[User, UserTable]):
    @staticmethod
    def to_entity(model: UserTable) -> User:
        return User(
            id=model.id,
            name=model.nombre,
            email=model.email,
            role=model.role,
            hashed_password=model.hashed_password,
            created_at=model.created_at,
            is_active=model.is_active
        )
    
    @staticmethod
    def to_db_model(user: User, user_db: UserTable | None = None) -> UserTable:
        if user_db:
            user_db.nombre = user.name
            user_db.email = user.email
            user_db.role = user.role
            user_db.hashed_password = user.hashed_password
            user_db.is_active = user.is_active
            return user_db
        return UserTable(
            nombre=user.name,
            email=user.email,
            role=user.role,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            created_at=user.created_at
        )