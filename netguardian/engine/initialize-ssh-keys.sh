#!/usr/bin/env sh
set -eu
mkdir -p /app/ssh
if [ ! -f /app/ssh/id_rsa ]; then
  ssh-keygen -t rsa -b 4096 -N "" -f /app/ssh/id_rsa
fi
chmod 700 /app/ssh
chmod 600 /app/ssh/id_rsa
chmod 644 /app/ssh/id_rsa.pub
