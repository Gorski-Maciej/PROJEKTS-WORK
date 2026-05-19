FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir confluent-kafka
COPY agent.py /app/agent.py

CMD ["python", "agent.py"]
