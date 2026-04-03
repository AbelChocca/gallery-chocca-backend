from dataclasses import dataclass

@dataclass
class RegisterUserCommand:
    name: str
    email: str
    password: str

@dataclass
class LoginUserCommand:
    email: str
    password: str