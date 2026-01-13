from app.api.schemas.user.schema_model import ReadUserSchema, LoginUserSchema, RegisterUserSchema
from app.application.user.commands import LoginUserCommand, RegisterUserCommand
from app.domain.user.dto import ReadUserDTO


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


class OutputSchemaMapper:
    @staticmethod
    def to_read_schema(dto: ReadUserDTO) -> ReadUserSchema:
        return ReadUserSchema(
            id=dto.id,
            nombre=dto.nombre,
            email=dto.email,
            role=dto.role
        )