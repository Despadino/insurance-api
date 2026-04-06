FROM python:3.12.4-slim

WORKDIR /app/src
COPY pyproject.toml poetry.lock ./

RUN pip install poetry==1.8.2 && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root

COPY . .