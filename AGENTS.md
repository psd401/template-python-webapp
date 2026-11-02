# AGENTS.md — template-python-webapp

Map, not manual. Change this file in the same PR that changes the convention.

## Commands (exact)

```bash
uv sync                     # install deps into .venv (uv.lock is committed)
uv run pytest               # tests (CI gate; zero-test repos fail psd-ci)
uv run ruff check           # lint
uv run ruff check --fix     # lint with autofix
uv run ruff format          # format
uv run ruff format --check  # CI format gate
uv run mypy                 # typecheck (strict; files = src + tests)
uv run uvicorn app.main:app --reload  # dev server on :8000
docker compose up --build   # containerized dev with live reload
docker build -t psd-webapp .          # production image
```

## Conventions

- **`uv run` everything** — bare `python`/`pip` is never correct here. Single-file scripts use PEP 723 inline metadata.
- The TestClient needs the `httpx2` dev dependency, not `httpx` 0.x: starlette 1.6+ deprecated httpx 0.x.
- `docker-compose.yml` is for local dev only (source mount, `--reload`); production is the `Dockerfile` image.
- New routes: typed pydantic request/response models; constraints on `Field` at the edge, not `if` checks inside handlers.
- New settings: typed field on `Settings` + entry in `.env.example`, same PR. No `os.environ` outside `config.py`.
- Tests go through the TestClient with exact expected values; validation-error tests assert status 422 plus `loc`/`type`.
- Tests construct explicit `Settings` — never depend on the developer's `.env` or the `get_settings()` cache.
- Test-first for non-trivial logic; watch the test fail before making it pass. Existing tests are contracts: weakening or deleting an assertion must be declared in the PR body.
- Dependencies: `uv add` (runtime) / `uv add --dev` (dev) so `uv.lock` stays in sync; state why in the PR body.

## Anti-patterns (will fail review)

- `pip install`, `python script.py`, requirements.txt, or a hand-edited `uv.lock`.
- `os.environ`/`os.getenv` reads outside `config.py`; committing `.env` (only `.env.example` is committed).
- Untyped dict request/response bodies; handlers returning bare dicts instead of models.
- Deleting or skipping a failing test to get green; assertion-free tests.
- Running the container as root, or COPYing `.env` into the image.
- Untyped public functions, `# type: ignore` without an explanatory comment, broad `except Exception` that swallows errors.

## PR evidence bar

pytest + ruff check + ruff format --check + mypy output pasted in the PR; bug fixes include a failing-then-passing test.
