FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /uvx /bin/

WORKDIR /service

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/service/.venv

COPY ./services/api/pyproject.toml ./services/api/uv.lock /service/
COPY ./services/server /server
RUN uv sync --frozen --no-install-project

COPY ./services/api/ /service/
COPY ./certs/ /service/certs/
RUN uv sync --frozen

ENV PATH="/service/.venv/bin:$PATH"

EXPOSE 8000
