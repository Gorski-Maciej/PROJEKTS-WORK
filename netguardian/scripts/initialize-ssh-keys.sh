#!/bin/bash
if [ ! -f /app/ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 2048 -f /app/ssh/id_rsa -N "" -q
    echo "SSH keys generated"
fi
