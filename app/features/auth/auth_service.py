from app.features.user.service import UserService
from app.features.cart.service import CartService
from app.api.security.hashing.hash_service import HashService
from app.api.security.jwt.jwt_service import JWTService
from app.core.settings.pydantic_settings import Settings

from app.features.auth.dto import RegisterUserCommand, LoginUserCommand
from app.core.exceptions import ValueNotFound

from app.api.security.exceptions import AuthException
from app.core.authorization.role_permissions import ROLE_PERMISSIONS

from app.features.consents.consent_service import ConsentService
from app.features.consents.exceptions import TermsNotAcceptedError

class AuthService:
    def __init__(
        self,
        user_service: UserService,
        hasher_service: HashService,
        cart_service: CartService,
        jwt_service: JWTService,
        consent_service: ConsentService,
        settings: Settings
    ):
        self._user_service = user_service
        self._hasher_service = hasher_service
        self._cart_service = cart_service
        self._jwt_service = jwt_service
        self.consent_service = consent_service
        self._settings = settings

    def logout_user(self) -> dict:
        """
        Handles user logout by verifying the presence of a valid token
        and removing JWT cookies from the response.
        """
        try:
            self._jwt_service.get_token_from_cookies()

        except ValueNotFound:
            ...

        self._jwt_service.delete_cookie("session_token")
        self._jwt_service.delete_cookie("refresh_token")

        return {"message": "Logout was successful!"}
    
    async def login_user(self, command: LoginUserCommand, anon_session_id: str) -> dict[str, str]:
        user = await self._user_service.get_user_by_email(command.email)

        if not self._hasher_service.verify(command.password, user.hashed_password):
            raise AuthException(
                "Password incorrect, retry.",
                {
                    "event": "login_user"
                }
            )
        
        payload: dict = {'sub': command.email, 'role': user.role}
        
        a_token = self._jwt_service.generate_token(payload)
        r_token = self._jwt_service.generate_token(payload, True)

        self._jwt_service.set_cookie(
            key="session_token",
            token=a_token,
            expires=self._settings.ACCESS_TOKEN_EXPIRES_SECONDS
        )
        self._jwt_service.set_cookie(
            key="refresh_token",
            token=r_token,
            expires=self._settings.REFRESH_TOKEN_EXPIRES_SECONDS
        )

        await self._cart_service.merge_guest_cart_to_user_cart(anon_session_id, user.id)
        return {"message": "Login successful"}
    
    async def register_user(
        self, 
        command: RegisterUserCommand,
        anon_session_id: int | None = None
    ) -> dict:
        if command.accepted_terms is not True:
            raise TermsNotAcceptedError(
                "Debes aceptar los términos y condiciones."
            )
        
        hashed_password = self._hasher_service.hash(command.password)

        user = await self._user_service.create_user(
            name=command.name,
            email=command.email,
            hashed_password=hashed_password,
            anon_session_id=anon_session_id
        )

        await self.consent_service.accept_terms(
            user_id=user.id,
            session_id=None,
        )

        return {
            "id": user.id,
            "nombre": user.name,
            "email": user.email,
            "role": user.role,
            "permissions": ROLE_PERMISSIONS[user.role]
        }