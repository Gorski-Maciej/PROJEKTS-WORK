FROM python:3.12-slim

WORKDIR /app

RUN useradd -m -u 1000 appuser

COPY api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY server/operational_mcp/ /app/server/operational_mcp/
COPY server/__init__.py /app/server/__init__.py

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health', timeout=3)" || exit 1

CMD ["uvicorn", "server.operational_mcp.app:app", "--host", "0.0.0.0", "--port", "8001"]
