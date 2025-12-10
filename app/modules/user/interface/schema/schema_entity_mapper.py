from app.modules.user.domain.user import User
from app.modules.user.interface.schema.schema import ReadUser

class SchemaEntityMapper:
    @staticmethod
    def to_schema(user: User) -> ReadUser:
        return ReadUser(
            id=user.id,
            nombre=user.name,
            email=user.email,
            role=user.role
        )