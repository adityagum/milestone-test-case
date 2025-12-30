FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq5 libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

# ⬇️ FIX PATH DEPENDENCY FILES
COPY services/order/pyproject.toml ./pyproject.toml
COPY services/order/poetry.lock ./poetry.lock

RUN poetry config virtualenvs.create false \
 && poetry install --only main --no-root --no-interaction --no-ansi

# ⬇️ FIX PATH SOURCE CODE
COPY services/order/app ./app
COPY shared ./shared

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
