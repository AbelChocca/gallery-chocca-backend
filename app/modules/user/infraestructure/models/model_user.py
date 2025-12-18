from sqlmodel import SQLModel, Field
from typing import Optional

# Modelo SQL para Admin
class UserTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, unique=True)
    email: str = Field(index=True, unique=True)
    role: str = Field(default='user',index=True, max_length=20)
    hashed_password: str
