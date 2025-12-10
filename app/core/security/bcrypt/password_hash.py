import bcrypt

from app.core.security.bcrypt.repository_passwordhash import PasswordHashRepository

class PasswordHasher(PasswordHashRepository):
    def hash(self, password: str) -> str:
        hashed = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
        return hashed.decode()
    
    def verify(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(), 
            hashed_password=hashed_password.encode()
            )

def get_hasher_repo() -> PasswordHashRepository:
    return PasswordHasher()
