import pytest
from unittest.mock import Mock, AsyncMock

from app.api.security.exceptions import SecurityException, AuthException
from app.api.security.jwt.jwt_exception import JWTException
from app.api.security.resolvers.sessions import SecuritySessions
from app.core.exceptions import ValueNotFound

class FakeUser:
    def __init__(self, id=1, name="Ana", email="a@a.com", role="user", is_active=True, created_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.is_active = is_active
        self.created_at = created_at

@pytest.fixture
def jwt_mock():
    jwt = Mock()
    jwt.get_token_from_cookies = Mock()
    jwt.get_session_token_from_cookies_with_no_raises = Mock()
    jwt.verify_token = Mock()
    return jwt

@pytest.fixture
def user_repo_mock():
    repo = Mock()
    repo.get_by_email = AsyncMock()
    return repo

@pytest.fixture
def service(jwt_mock, user_repo_mock):
    return SecuritySessions(jwt=jwt_mock, user_repo=user_repo_mock)

@pytest.mark.asyncio
async def test__get_user_no_payload_raises_unauthorized(service, jwt_mock):
    jwt_mock.get_token_from_cookies.return_value = None

    with pytest.raises(AuthException):
        await service._get_user()

@pytest.mark.asyncio
async def test__get_user_returns_user(service, jwt_mock, user_repo_mock):
    jwt_mock.get_token_from_cookies.return_value = {"sub": "a@a.com"}
    u = FakeUser(email="a@a.com")
    user_repo_mock.get_by_email.return_value = u

    user = await service._get_user()

    user_repo_mock.get_by_email.assert_awaited_once_with("a@a.com")
    assert user is u

@pytest.mark.asyncio
async def test_get_user_session_user_not_found_unauthorized(service, jwt_mock, user_repo_mock):
    jwt_mock.get_token_from_cookies.return_value = {"sub": "x@x.com"}
    user_repo_mock.get_by_email.return_value = None

    with pytest.raises(ValueNotFound):
        await service.get_user_session()

@pytest.mark.asyncio
async def test_get_user_session_inactive_forbidden(service, jwt_mock, user_repo_mock):
    jwt_mock.get_token_from_cookies.return_value = {"sub": "a@a.com"}
    user_repo_mock.get_by_email.return_value = FakeUser(is_active=False)

    with pytest.raises(SecurityException) as exc:
        await service.get_user_session()

    assert "not longer active" in str(exc.value)

@pytest.mark.asyncio
async def test_get_user_session_returns_dto(service, jwt_mock, user_repo_mock):
    jwt_mock.get_token_from_cookies.return_value = {"sub": "a@a.com"}
    u = FakeUser(id=7, name="Caro", email="a@a.com", role="user", is_active=True, created_at="2026-02-18")
    user_repo_mock.get_by_email.return_value = u

    dto = await service.get_user_session()

    assert dto["id"] == 7
    assert dto["nombre"] == "Caro"
    assert dto["email"] == "a@a.com"
    assert dto["role"] == "user"
    assert dto["is_active"] is True

@pytest.mark.asyncio
async def test_get_admin_non_admin_forbidden(service, jwt_mock, user_repo_mock):
    jwt_mock.get_token_from_cookies.return_value = {"sub": "a@a.com"}
    user_repo_mock.get_by_email.return_value = FakeUser(role="user", is_active=True)

    with pytest.raises(SecurityException):
        await service.get_admin()

@pytest.mark.asyncio
async def test_get_admin_returns_dto(service, jwt_mock, user_repo_mock):
    jwt_mock.get_token_from_cookies.return_value = {"sub": "admin@a.com"}
    user_repo_mock.get_by_email.return_value = FakeUser(id=1, name="Admin", email="admin@a.com", role="admin")

    dto = await service.get_admin()

    assert dto["role"] == "admin"
    assert dto["email"] == "admin@a.com"


@pytest.mark.asyncio
async def test_get_user_id_no_token_returns_none(service, jwt_mock):
    jwt_mock.get_session_token_from_cookies_with_no_raises.return_value = None

    user_id = await service.get_user_id()

    assert user_id is None

@pytest.mark.asyncio
async def test_get_user_id_invalid_payload_returns_none(service, jwt_mock):
    jwt_mock.get_session_token_from_cookies_with_no_raises.return_value = "tok"
    jwt_mock.verify_token.return_value = None

    user_id = await service.get_user_id()

    assert user_id is None

@pytest.mark.asyncio
async def test_get_user_id_user_not_found_returns_none(service, jwt_mock, user_repo_mock):
    jwt_mock.get_session_token_from_cookies_with_no_raises.return_value = "tok"
    jwt_mock.verify_token.return_value = {"sub": "a@a.com"}
    user_repo_mock.get_by_email.return_value = None

    user_id = await service.get_user_id()

    assert user_id is None

@pytest.mark.asyncio
async def test_get_user_id_returns_id(service, jwt_mock, user_repo_mock):
    jwt_mock.get_session_token_from_cookies_with_no_raises.return_value = "tok"
    jwt_mock.verify_token.return_value = {"sub": "a@a.com"}
    user_repo_mock.get_by_email.return_value = FakeUser(id=99)

    assert service.user_repo is user_repo_mock

    user_id = await service.get_user_id()

    assert user_id == 99
    jwt_mock.verify_token.assert_called_once_with("tok")
    user_repo_mock.get_by_email.assert_awaited_once_with("a@a.com")
