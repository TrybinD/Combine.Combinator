FROM python:3.10-slim as builder

RUN pip install poetry
RUN mkdir -p /app
RUN mkdir -p /app/models

COPY pyproject.toml /app
COPY poetry.lock /app
COPY main.py /app
COPY ./src /app/src
COPY ./data /app/data

WORKDIR /app
RUN poetry config virtualenvs.in-project true
RUN poetry install

FROM python:3.10-slim as base

COPY --from=builder /app /app

WORKDIR /app

CMD [".venv/bin/python", "main.py"]