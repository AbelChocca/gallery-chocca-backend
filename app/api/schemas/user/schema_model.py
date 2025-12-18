from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import  Optional

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class RegisterUserSchema(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Optional[str] = 'user'

class ReadUserSchema(BaseModel):
    id: int
    nombre: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)
