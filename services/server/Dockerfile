FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /uvx /bin/

WORKDIR /service

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/service/.venv

COPY ./services/server/pyproject.toml ./services/server/uv.lock /service/
RUN uv sync --frozen --no-install-project

COPY ./services/server/ /service/
COPY ./certs/ /service/certs/
RUN uv sync --frozen

ENV PATH="/service/.venv/bin:$PATH"

EXPOSE 50051
EXPOSE 50052
EXPOSE 50053
