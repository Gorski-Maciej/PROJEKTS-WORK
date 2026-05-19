#!/bin/bash
cp -n .env.example .env 2>/dev/null || true
docker compose build
docker compose up -d
echo "InfraFlow started at http://localhost:8001"
