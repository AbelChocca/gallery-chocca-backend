from pydantic import BaseModel, constr, EmailStr, ConfigDict
from typing import Annotated, Optional

class LoginUser(BaseModel):
    email: EmailStr
    password: Annotated[str, constr(min_length=8, max_length=128)]

class RegisterUser(BaseModel):
    nombre: Annotated[str, constr(min_length=2, max_length=50)]
    email: EmailStr
    password: Annotated[str, constr(min_length=8, max_length=128)]
    role: Optional[str] = 'user'

class ReadUser(BaseModel):
    id: int
    nombre: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)
