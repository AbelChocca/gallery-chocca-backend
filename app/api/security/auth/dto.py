from dataclasses import dataclass

@dataclass(frozen=True)
class RegisterUserCommand:
    name: str
    email: str
    password: str

@dataclass(frozen=True)
class LoginUserCommand:
    email: str
    password: str