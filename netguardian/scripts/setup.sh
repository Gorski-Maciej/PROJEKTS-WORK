#!/bin/bash
cp -n .env.example .env 2>/dev/null || true
if [ ! -f engine/ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 2048 -f engine/ssh/id_rsa -N "" -q
fi
docker compose build
docker compose up -d
echo "NetGuardian started at http://localhost:8300"
