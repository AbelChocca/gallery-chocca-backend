from types import SimpleNamespace
import pytest
from fastapi import HTTPException
from app.api.security.exceptions import AuthException

from app.api.security.resolvers.session_owner import (
    get_session_owner,
    OwnerSession
)

def make_request_with_cookies(cookies: dict):
    return SimpleNamespace(cookies=cookies)

def test_owner_is_user_when_user_is_present():
    req = make_request_with_cookies({"anon_session_id": "abc"})
    owner = get_session_owner(req, user_id=123)

    assert isinstance(owner, OwnerSession)
    assert owner.is_user is True
    assert owner.user_id == 123
    assert owner.session_id is None

def test_owner_is_anon_when_user_id_none_and_cookie_present():
    req = make_request_with_cookies({"anon_session_id": "anon-xyz"})
    owner = get_session_owner(request=req, user_id=None)

    assert owner.is_user is False
    assert owner.user_id is None
    assert owner.session_id == "anon-xyz"

def test_non_owner():
    req = make_request_with_cookies({})
    with pytest.raises(AuthException) as exc:
        get_session_owner(req, None)

        assert exc.value.status_code == 401