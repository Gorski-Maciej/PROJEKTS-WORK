FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends iptables openssh-server \
    && mkdir /var/run/sshd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN useradd -m -u 1000 appuser

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY agent.py ./agent.py

RUN chown -R appuser:appuser /app
USER appuser

HEALTHCHECK --interval=20s --timeout=5s --retries=3 \
  CMD python -c "import psutil; psutil.Process().status()" || exit 1

CMD ["python", "agent.py"]
