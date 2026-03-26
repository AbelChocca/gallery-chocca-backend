from app.api.schemas.user.user_schema import LoginUserSchema, RegisterUserSchema
from app.domain.user.dto import LoginUserCommand, RegisterUserCommand


class InputSchemaMapper:
    @staticmethod
    def to_login_command(schema: LoginUserSchema) -> LoginUserCommand:
        return LoginUserCommand(
            email=schema.email,
            password=schema.password
        )
    @staticmethod
    def to_register_command(schema: RegisterUserSchema) -> RegisterUserCommand:
        return RegisterUserCommand(
            nombre=schema.nombre,
            email=schema.email,
            password=schema.password,
            role=schema.role
        )