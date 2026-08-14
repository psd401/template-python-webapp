"""Tests for app.config.Settings - environment-driven loading and validation."""

import pytest
from pydantic import ValidationError

from app.config import Settings
from app.main import create_app

_APP_VARS = ("APP_TITLE", "APP_ENVIRONMENT", "APP_DEBUG")


def test_defaults_when_environment_is_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in _APP_VARS:
        monkeypatch.delenv(var, raising=False)
    settings = Settings(_env_file=None)
    assert settings.title == "psd-webapp"
    assert settings.environment == "development"
    assert settings.debug is False


def test_reads_app_prefixed_environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_TITLE", "attendance-api")
    monkeypatch.setenv("APP_ENVIRONMENT", "production")
    monkeypatch.setenv("APP_DEBUG", "true")
    settings = Settings(_env_file=None)
    assert settings.title == "attendance-api"
    assert settings.environment == "production"
    assert settings.debug is True


def test_rejects_unknown_environment_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENVIRONMENT", "staging")
    with pytest.raises(ValidationError, match="environment"):
        Settings(_env_file=None)


def test_create_app_applies_settings() -> None:
    settings = Settings(_env_file=None, title="my-service", debug=True)
    app = create_app(settings)
    assert app.title == "my-service"
    assert app.debug is True
