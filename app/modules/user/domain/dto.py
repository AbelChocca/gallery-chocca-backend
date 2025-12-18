from dataclasses import dataclass

@dataclass
class ReadUserDTO:
    id: int
    nombre: str
    email: str
    role: str