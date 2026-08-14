"""Tests for app.main routes - exact-value assertions (standards/05-testing.md)."""

from fastapi.testclient import TestClient


def test_healthz_returns_ok(client: TestClient) -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_reading_time_happy_path(client: TestClient) -> None:
    # 6 words at 4 words/minute -> ceil(6/4) = 2 minutes.
    response = client.post(
        "/api/reading-time",
        json={"text": "one two three four five six", "words_per_minute": 4},
    )
    assert response.status_code == 200
    assert response.json() == {"words": 6, "minutes": 2}


def test_reading_time_uses_default_words_per_minute(client: TestClient) -> None:
    # 300 words at the default 200 wpm -> ceil(300/200) = 2 minutes.
    response = client.post("/api/reading-time", json={"text": "word " * 300})
    assert response.status_code == 200
    assert response.json() == {"words": 300, "minutes": 2}


def test_reading_time_whitespace_only_text_yields_zero(client: TestClient) -> None:
    response = client.post("/api/reading-time", json={"text": "  \n\t  "})
    assert response.status_code == 200
    assert response.json() == {"words": 0, "minutes": 0}


def test_reading_time_rejects_out_of_range_words_per_minute(client: TestClient) -> None:
    response = client.post(
        "/api/reading-time",
        json={"text": "hello", "words_per_minute": 0},
    )
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "words_per_minute"]
    assert error["type"] == "greater_than_equal"


def test_reading_time_rejects_missing_text(client: TestClient) -> None:
    response = client.post("/api/reading-time", json={"words_per_minute": 100})
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "text"]
    assert error["type"] == "missing"
