from pydantic import BaseModel, Field, EmailStr, ConfigDict
from app.core.authorization.permissions import Permission
from app.features.user.types import UserRole

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class RegisterUserSchema(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    captchaToken: str

class ReadSessionSchema(BaseModel):
    id: int | None = None
    role: UserRole
    permissions: list[Permission]

    model_config = ConfigDict(from_attributes=True)