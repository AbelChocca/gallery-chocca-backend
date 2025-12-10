from app.modules.user.interface.schema.schema import LoginUser, RegisterUser
from app.shared.dto.user_dto import LoginUserDTO, RegisterUserDTO

class DTOUserMapper:
    @staticmethod
    def login_mapper(schema: LoginUser) -> LoginUserDTO:
        return LoginUserDTO(
            email=schema.email,
            password=schema.password
        )
    
    @staticmethod
    def register_mapper(schema: RegisterUser) -> RegisterUserDTO:
        return RegisterUserDTO(
            nombre=schema.nombre,
            email=schema.email,
            role=schema.role,
            password=schema.password
        )