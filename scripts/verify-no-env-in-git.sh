#!/bin/bash
if git ls-files "**/.env" | grep -q .; then
    echo "ERROR: .env files tracked by Git"
    exit 1
fi
echo ".env files not in Git - OK"
