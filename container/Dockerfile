FROM node:21.7.2-bookworm-slim as frontend-builder

WORKDIR /app

COPY ./frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY ./frontend ./
RUN npm run make-i18n && npm run build

FROM python:3.12-slim as python-builder

RUN apt-get update -y \
    && apt-get install -y build-essential \
    && python3 -m pip install poetry  --break-system-packages \
    && poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true

COPY ./pyproject.toml ./poetry.lock ./
ENV POETRY_REQUESTS_TIMEOUT=300
ENV PIP_DEFAULT_TIMEOUT=300
RUN poetry install --without evaluation

FROM python:3.12-slim as runtime

WORKDIR /app
ENV PYTHONPATH '/app'
ENV RUN_AS_DEVIN=false
ENV USE_HOST_NETWORK=false
ENV SSH_HOSTNAME=host.docker.internal
ENV WORKSPACE_BASE=/opt/workspace_base
RUN mkdir -p $WORKSPACE_BASE

RUN apt-get update -y \
    && apt-get install -y curl make git \
    && python3 -m pip install poetry  --break-system-packages \
    && poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true

COPY --from=frontend-builder /app/dist ./frontend/dist
COPY --from=python-builder /app /app

COPY ./opendevin ./opendevin
COPY ./agenthub ./agenthub
RUN poetry run python opendevin/download.py # No-op to download assets

CMD ["poetry", "run", "uvicorn", "opendevin.server.listen:app", "--host", "0.0.0.0", "--port", "3000"]
