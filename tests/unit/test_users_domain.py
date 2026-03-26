# test_user_domain.py
import pytest
from datetime import datetime
from app.domain.user.entity import User
from app.core.exceptions import ValidationError

# ------------------------
# 1️⃣ Test creación básica
# ------------------------
def test_user_creation():
    user = User(
        name="Cerdito",
        email="cerdito@example.com",
        hashed_password="hashed123",
        is_active=True,
        role="admin"
    )
    assert user.name == "Cerdito"
    assert user.email == "cerdito@example.com"
    assert user.hashed_password == "hashed123"
    assert user.is_active is True
    assert user.role == "admin"
    assert isinstance(user.created_at, datetime)

# ------------------------
# 2️⃣ Test toggle_active
# ------------------------
def test_toggle_active():
    user = User("Name", "email@test.com", "pass")
    user.toggle_active(False)
    assert user.is_active is False
    user.toggle_active(True)
    assert user.is_active is True

# ------------------------
# 3️⃣ Test change_email
# ------------------------
def test_change_email_success():
    user = User("Name", "old@test.com", "pass")
    user.change_email("new@test.com")
    assert user.email == "new@test.com"

def test_change_email_same_email():
    user = User("Name", "same@test.com", "pass")
    with pytest.raises(ValidationError):
        user.change_email("same@test.com")

# ------------------------
# 4️⃣ Test change_password
# ------------------------
def test_change_password():
    user = User("Name", "email@test.com", "oldpass")
    user.change_password("newpass")
    assert user.hashed_password == "newpass"