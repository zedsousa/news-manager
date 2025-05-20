FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "news_manager.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
