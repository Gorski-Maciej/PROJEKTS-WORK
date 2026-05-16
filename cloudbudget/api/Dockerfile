FROM python:3.12-slim
WORKDIR /app
COPY ../pyproject.toml /app/pyproject.toml
COPY . /app/api
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg[binary] pydantic celery redis duckdb polars prophet scikit-learn prometheus-client python-jose[cryptography] passlib[bcrypt]
ENV PYTHONPATH=/app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
