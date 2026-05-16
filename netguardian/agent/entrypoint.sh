#!/bin/bash
set -e

ssh-keygen -A
/usr/sbin/sshd
exec python /app/agent.py
