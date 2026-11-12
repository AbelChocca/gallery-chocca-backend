import pytest_asyncio

from app.infra.db.models.model_user import UserTable
from app.features.user.types import UserRole
from app.api.security.hashing.hash_service import get_hasher_service

@pytest_asyncio.fixture(
    scope="function",
    loop_scope="session",
)
async def admin_user(
    db_session,
):
    password = "Admin1234!"

    hash_service = get_hasher_service()

    admin = UserTable(
        nombre="admin-e2e",
        email="admin-e2e@test.com",
        role=UserRole.ADMIN,
        hashed_password=hash_service.hash(password),
        is_active=True,
    )

    db_session.add(admin)

    await db_session.commit()
    await db_session.refresh(admin)

    return {
        "user": admin,
        "password": password,
    }