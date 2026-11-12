from fastapi import Request

from app.core.settings.pydantic_settings import settings


def get_client_ip(
    request: Request,
) -> str:
    return "179.6.137.194"

    if (
        settings.ENVIRONMENT == "development"
        and settings.OPENPAY_TEST_CLIENT_IP
    ):
        return settings.OPENPAY_TEST_CLIENT_IP

    forwarded_for = request.headers.get(
        "x-forwarded-for"
    )

    if forwarded_for:
        return (
            forwarded_for
            .split(",")[0]
            .strip()
        )

    if request.client:
        return request.client.host

    return "127.0.0.1"