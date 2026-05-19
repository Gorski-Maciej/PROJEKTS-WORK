FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8300

ENTRYPOINT ["/bin/sh", "-c", "./initialize-ssh-keys.sh && ./download_geoip.sh && uvicorn engine.main:app --host 0.0.0.0 --port 8300"]
