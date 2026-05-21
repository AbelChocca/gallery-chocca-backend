from app.api.security.auth.auth_service import AuthService
from app.features.user.dependency import get_user_service
from app.features.user.service import UserService
from app.api.security.hashing.hash_service import HashService, get_hasher_service
from app.api.security.jwt.jwt_service import JWTService, get_jwt_service

from fastapi import Depends

def get_auth_service(
        user_service: UserService = Depends(get_user_service),
        hash_service: HashService = Depends(get_hasher_service),
        jwt_service: JWTService = Depends(get_jwt_service)
        ) -> AuthService:
    return AuthService(
        user_service=user_service,
        hasher_service=hash_service,
        jwt_service=jwt_service
    )