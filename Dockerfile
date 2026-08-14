# syntax=docker/dockerfile:1
# Multi-stage build: uv resolves and installs into a virtualenv, the slim
# runtime stage copies only that virtualenv and runs as a non-root user.

# ---- build stage -----------------------------------------------------------
# ghcr.io/astral-sh/uv images are built on the matching python:*-slim image,
# so the virtualenv's interpreter path resolves identically in both stages.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

# Dependency layer - cached until pyproject.toml/uv.lock change.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Project layer - the app itself, installed non-editable into the venv
# (README.md is required: pyproject.toml references it as package metadata).
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# ---- runtime stage ---------------------------------------------------------
FROM python:3.12-slim-bookworm

RUN groupadd --system app && useradd --system --gid app app

WORKDIR /app
COPY --from=builder --chown=app:app /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

USER app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
