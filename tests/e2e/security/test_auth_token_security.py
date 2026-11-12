
import base64
import json

import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio(
    loop_scope="session",
)
AUTH_COOKIE_NAME = "session_token"

PROTECTED_URL = "/product/delete/2147483647"

UNAUTHORIZED_STATUS_CODES = (401, 403)

def replace_session_token(
    client: AsyncClient,
    token: str,
) -> None:
    client.cookies.clear()

    client.cookies.set(
        "session_token",
        token,
    )

def get_auth_token(client: AsyncClient) -> str:
    token = client.cookies.get(AUTH_COOKIE_NAME)

    assert token, (
        f"No se encontró la cookie {AUTH_COOKIE_NAME!r}. "
        f"Cookies disponibles: {list(client.cookies.keys())}"
    )

    return token


def tamper_token(token: str) -> str:
    """Altera un token sin conocer la clave de firma."""

    parts = token.split(".")

    if len(parts) == 3:
        # JWT: modificar la firma sin cambiar header/payload.
        signature = parts[2]

        assert signature, "JWT sin firma"

        replacement = (
            "A" if signature[0] != "A" else "B"
        )

        parts[2] = replacement + signature[1:]

        return ".".join(parts)

    # Token opaco u otro formato.
    return token + "-tampered"


def unsigned_jwt() -> str:
    """Construye un JWT con alg=none (sin firma)."""

    def encode(data: dict) -> str:
        raw = json.dumps(
            data,
            separators=(",", ":"),
        ).encode()

        return (
            base64.urlsafe_b64encode(raw)
            .rstrip(b"=")
            .decode()
        )

    return (
        f"{encode({'alg': 'none', 'typ': 'JWT'})}."
        f"{encode({'sub': '1', 'exp': 4102444800})}."
    )


async def assert_access_denied(
    client: AsyncClient,
) -> None:
    response = await client.delete(PROTECTED_URL)

    assert response.status_code in (
        UNAUTHORIZED_STATUS_CODES
    ), response.text


async def test_valid_admin_token_is_accepted_e2e(
    admin_client: AsyncClient,
):
    token = get_auth_token(admin_client)

    assert token

    response = await admin_client.delete(
        PROTECTED_URL
    )

    assert response.status_code == 404, response.text



async def test_missing_token_is_rejected_e2e(
    http_client: AsyncClient,
):
    http_client.cookies.clear()

    await assert_access_denied(http_client)



async def test_random_invalid_token_is_rejected_e2e(
    admin_client: AsyncClient,
):
    replace_session_token(
        admin_client,
        "invalid-token-without-valid-signature",
    )

    await assert_access_denied(admin_client)


async def test_tampered_token_is_rejected_e2e(
    admin_client: AsyncClient,
):
    original_token = get_auth_token(admin_client)

    replace_session_token(
        admin_client,
        tamper_token(original_token),
    )

    await assert_access_denied(admin_client)



async def test_empty_token_is_rejected_e2e(
    admin_client: AsyncClient,
):
    replace_session_token(
        admin_client,
        "",
    )

    await assert_access_denied(admin_client)


async def test_unsigned_jwt_is_rejected_e2e(
    admin_client: AsyncClient,
):
    replace_session_token(
        admin_client,
        unsigned_jwt(),
    )

    await assert_access_denied(admin_client)