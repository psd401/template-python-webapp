"""Runtime configuration - pydantic-settings, environment-driven.

Settings load from (highest precedence first) real environment variables,
then a local ``.env`` file. Every variable carries the ``APP_`` prefix;
``.env.example`` is the committed reference. All environment reads live in
this module - handlers and services take a ``Settings`` instance, never
``os.environ``.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings - one typed attribute per ``APP_*`` variable."""

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    title: str = "psd-webapp"
    environment: Literal["development", "test", "production"] = "development"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide :class:`Settings` (cached after first load).

    Tests bypass this cache by constructing ``Settings(_env_file=None, ...)``
    and passing it to :func:`app.main.create_app` directly.
    """
    return Settings()
