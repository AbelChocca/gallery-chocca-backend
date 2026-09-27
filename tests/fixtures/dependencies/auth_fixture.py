import pytest_asyncio

from httpx import AsyncClient

@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def admin_client(
    http_client: AsyncClient,
    admin_user,
) -> AsyncClient:

    http_client.cookies.clear()

    admin = admin_user["user"]
    password = admin_user["password"]

    response = await http_client.post(
        "/auth/login",
        json={
            "email": admin.email,
            "password": password,
        },
    )

    assert response.status_code == 200

    return http_client