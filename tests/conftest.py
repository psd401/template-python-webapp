"""Shared fixtures - a TestClient against an app built from explicit Settings.

The fixture constructs ``Settings(_env_file=None, ...)`` so tests are immune
to a developer's local ``.env`` file and to the ``get_settings()`` cache.
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """HTTP client against an app configured for tests."""
    settings = Settings(_env_file=None, environment="test")
    with TestClient(create_app(settings)) as test_client:
        yield test_client
