from dataclasses import dataclass

@dataclass
class RegisterUserDTO:
    nombre: str
    email: str
    role: str
    password: str

@dataclass
class LoginUserDTO:
    email: str
    password: str