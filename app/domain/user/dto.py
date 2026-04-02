from dataclasses import dataclass

@dataclass
class RegisterUserCommand:
    name: str
    email: str
    password: str
    role: str

@dataclass
class LoginUserCommand:
    email: str
    password: str