import pytest


@pytest.fixture(autouse=True)
def mock_complaints_mail(fake_mail_service):
    yield