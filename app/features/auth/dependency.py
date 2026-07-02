from app.features.auth.auth_service import AuthService
from app.features.user.dependency import get_user_service
from app.features.user.service import UserService
from app.api.security.hashing.hash_service import HashService, get_hasher_service
from app.features.cart.dependency import get_cart_service
from app.features.cart.service import CartService
from app.api.security.jwt.jwt_service import JWTService, get_jwt_service
from app.core.settings.pydantic_settings import Settings, get_settings

from fastapi import Depends

def get_auth_service(
        user_service: UserService = Depends(get_user_service),
        hash_service: HashService = Depends(get_hasher_service),
        jwt_service: JWTService = Depends(get_jwt_service),
        cart_service: CartService = Depends(get_cart_service),
        settings: Settings = Depends(get_settings)
        ) -> AuthService:
    return AuthService(
        user_service=user_service,
        hasher_service=hash_service,
        jwt_service=jwt_service,
        cart_service=cart_service,
        settings=settings
    )