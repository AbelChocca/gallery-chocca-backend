from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import  List
from datetime import datetime
from app.api.schemas.pagination import PaginationResponseSchema

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class RegisterUserSchema(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: str | None = 'user'
    captchaToken: str

class ReadSessionSchema(BaseModel):
    id: int | None = None
    role: str

    model_config = ConfigDict(from_attributes=True)

class ReadUserSchema(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime | None = None
    role: str

    model_config = ConfigDict(from_attributes=True)

class GetUsersResponseSchema(BaseModel):
    users: List[ReadUserSchema]
    pagination: PaginationResponseSchema
    total_items: int