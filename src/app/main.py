"""FastAPI application - app factory plus the template's example route.

Replace the reading-time endpoint with your real routes; keep the pattern:
typed pydantic request/response models, validation at the edge via ``Field``
constraints, and real tests through the TestClient.
"""

import math
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.config import Settings, get_settings


class HealthResponse(BaseModel):
    """Response body for ``GET /healthz``."""

    status: Literal["ok"]


class ReadingTimeRequest(BaseModel):
    """Request body for ``POST /api/reading-time``."""

    text: str = Field(description="Text to estimate reading time for.")
    words_per_minute: int = Field(
        default=200, ge=1, le=2000, description="Reading speed, 1-2000 words per minute."
    )


class ReadingTimeResponse(BaseModel):
    """Response body for ``POST /api/reading-time``."""

    words: int
    minutes: int


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the FastAPI application.

    Args:
        settings: Explicit settings (tests construct their own); ``None``
            falls back to the cached environment-driven instance.

    Returns:
        A configured :class:`fastapi.FastAPI` app.
    """
    if settings is None:
        settings = get_settings()

    app = FastAPI(title=settings.title, debug=settings.debug)

    @app.get("/healthz")
    def healthz() -> HealthResponse:
        """Liveness probe for containers and load balancers."""
        return HealthResponse(status="ok")

    @app.post("/api/reading-time")
    def reading_time(payload: ReadingTimeRequest) -> ReadingTimeResponse:
        """Estimate reading time for a block of text.

        Whitespace-only text yields zero words and zero minutes; any text
        with at least one word takes at least one minute (ceiling division).
        """
        words = len(payload.text.split())
        minutes = 0 if words == 0 else math.ceil(words / payload.words_per_minute)
        return ReadingTimeResponse(words=words, minutes=minutes)

    return app


app = create_app()
