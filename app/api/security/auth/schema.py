from pydantic import BaseModel, Field, EmailStr, ConfigDict

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
    role: str

    model_config = ConfigDict(from_attributes=True)