FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY engine/ ./engine/
EXPOSE 8300
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8300/health')"
CMD ["uvicorn", "engine.main:app", "--host", "0.0.0.0", "--port", "8300"]
