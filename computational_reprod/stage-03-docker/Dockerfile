# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:0.11.33 AS uv

FROM python:3.11-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
COPY --from=uv /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    MPLCONFIGDIR=/tmp/matplotlib
RUN groupadd --system app && useradd --system --gid app --create-home app
WORKDIR /app
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app src ./src
COPY --chown=app:app run_analysis.py ./run_analysis.py
RUN mkdir -p /data/input /data/output && chown -R app:app /data
USER app

ENTRYPOINT ["/app/.venv/bin/python", "/app/run_analysis.py"]
CMD ["--input", "/data/input/data.csv", "--output", "/data/output", "--predict-temperature", "40"]
