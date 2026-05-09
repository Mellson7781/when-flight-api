FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

ENV POETRY_VIRTUALENVS_CREATE=false

RUN poetry install --no-interaction --no-root

COPY . .

EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]