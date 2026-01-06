from app.modules.user.domain.user import User
from app.infra.db.models.model_user import UserTable

from typing import Optional

class UserMapper:
    @staticmethod
    def to_entity(user_db: UserTable) -> User:
        return User(
            id=user_db.id,
            name=user_db.nombre,
            email=user_db.email,
            role=user_db.role,
            hashed_password=user_db.hashed_password
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