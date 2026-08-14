# template-python-webapp

PSD401 template for containerized Python web apps. FastAPI + uv + Docker, src layout, Python 3.12+.

## What this template gives you

- **FastAPI app factory** (`src/app/main.py`): `create_app()` with a `/healthz` liveness probe and one real example route (`POST /api/reading-time`) using typed pydantic request/response models with `Field` validation at the edge.
- **Environment-driven config** (`src/app/config.py`): pydantic-settings with `APP_` prefix, `.env` support, and a committed `.env.example`. All environment reads live in one module.
- **Tests that mean something**: pytest + httpx TestClient (via `httpx2` — starlette 1.6+ deprecated the httpx 0.x line) — healthz, happy path with exact values, two 422 validation paths, and config loading (defaults, env override, invalid value, factory wiring). PSD CI fails zero-test repos by design.
- **ruff** (lint + format, line length 100, `E W F I UP B SIM RUF`) and **mypy strict** (pydantic plugin) over `src` + `tests`, both configured in `pyproject.toml`.
- **Docker**: multi-stage Dockerfile (uv builder → `python:3.12-slim` runtime, non-root user, only the venv copied), `docker-compose.yml` for live-reload local dev, `.dockerignore`.
- **PSD CI wiring** (org reusable workflows), Dependabot (github-actions + uv, weekly, minor/patch grouped), MIT LICENSE, CLAUDE.md.

## The PSD runtime rule

Everything runs through uv — never bare `python` or `pip`:

```bash
uv run pytest          # not: python -m pytest
uv run some_script.py  # not: python some_script.py
```

## First 10 minutes

1. **Rename**: `name` in `pyproject.toml`, the `src/app/` package directory, the `[tool.hatch.build.targets.wheel]` packages entry, imports in `tests/`, and the `app.main:app` references in `Dockerfile` and `docker-compose.yml`. Naming: lowercase-kebab repo, snake_case package, `psd-` prefix for district-specific apps.
2. **Set repo custom properties**: `tier` (default `c-experiment`), `owner`, `lifecycle: active`; add topics (`python`, `fastapi`, …).
3. **Configure**: `cp .env.example .env`, adjust values; add new settings as typed fields on `Settings` plus a line in `.env.example`.
4. **Review CLAUDE.md** and prune it to your app.
5. **Verify green**: `uv sync && uv run pytest && uv run ruff check && uv run ruff format --check && uv run mypy`.
6. **Verify the container**: `docker build -t my-app .` then `docker compose up --build` and hit <http://localhost:8000/healthz>.
7. Replace the reading-time route and its tests with your real endpoints — never leave the repo with zero tests.

## Commands

| Task | Command |
|------|---------|
| Install/sync | `uv sync` |
| Test | `uv run pytest` |
| Lint | `uv run ruff check` |
| Format | `uv run ruff format` |
| Format check (CI) | `uv run ruff format --check` |
| Typecheck | `uv run mypy` |
| Dev server | `uv run uvicorn app.main:app --reload` |
| Dev in Docker | `docker compose up --build` |
| Production image | `docker build -t psd-webapp .` |

## Owner

Technology Services, Peninsula School District.
