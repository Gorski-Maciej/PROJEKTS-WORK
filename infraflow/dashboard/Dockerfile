FROM python:3.12-slim

WORKDIR /app

RUN useradd -m -u 1000 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard/ ./dashboard/

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8081

CMD ["python", "dashboard/main.py"]
