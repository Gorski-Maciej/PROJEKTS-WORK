#!/bin/bash
for proj in cloudbudget infraflow netguardian netaegis; do
    cd "$proj"
    cp -n .env.example .env 2>/dev/null || echo ".env already exists in $proj"
    cd ..
done
echo "Configuration prepared"
