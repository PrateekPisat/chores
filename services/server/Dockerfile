FROM python:3.12

RUN mkdir /service

#  Configure Poetry
ENV POETRY_VERSION=1.8.3 \ 
    POETRY_HOME=/opt/poetry \
    POETRY_VENV=/opt/poetry-venv \
    POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"
    
COPY ./services/server/poetry.lock ./services/server/pyproject.toml /service/

WORKDIR /service/
RUN poetry install

COPY ./services/server/ /service/
COPY ../../certs/ /service/certs/
RUN poetry install

EXPOSE 50051
EXPOSE 50052
EXPOSE 50053