import httpx

from app.core.settings.pydantic_settings import settings
from app.api.security.exceptions import InvalidCaptcha
from app.api.schemas.user.user_schema import RegisterUserSchema


async def verify_captcha(payload: RegisterUserSchema) -> RegisterUserSchema:
    url = "https://www.google.com/recaptcha/api/siteverify"

    async with httpx.AsyncClient() as client:
        res = await client.post(
            url,
            data={
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": payload.captchaToken
            }
        )
    
    data: dict = res.json()

    if not data.get("success"):
        raise InvalidCaptcha(
            "Invalid captcha, retry",
            {
                "event": "verify_captcha",
                "success": data.get("success"),
                "score": data.get("score"),
                "action": data.get("action"),
                "hostname": data.get("hostname"),
            }
        )
    
    return payload