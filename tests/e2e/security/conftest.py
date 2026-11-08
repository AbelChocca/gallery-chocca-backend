
import pytest

from types import SimpleNamespace

from fastapi import Request

from app.main import app


@pytest.fixture
def bypass_captcha():
    register_route = next(
        route
        for route in app.routes
        if getattr(route, "path", None) == "/auth/register"
        and "POST" in getattr(route, "methods", set())
    )

    captcha_dependency = next(
        dependency.call
        for dependency in register_route.dependant.dependencies
        if getattr(dependency.call, "__name__", "")
        == "verify_captcha"
    )

    async def fake_verify_captcha(request: Request):
        payload = await request.json()

        # Esta sustitución se limita al CAPTCHA.
        # El endpoint recibirá los datos enviados.
        return SimpleNamespace(**payload)

    app.dependency_overrides[
        captcha_dependency
    ] = fake_verify_captcha

    yield

    app.dependency_overrides.pop(
        captcha_dependency,
        None,
    )
