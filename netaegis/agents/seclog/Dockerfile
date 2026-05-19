FROM python:3.12-slim

WORKDIR /app

COPY agents/seclog/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY agents /app/agents

CMD ["python", "-m", "agents.seclog.agent"]
