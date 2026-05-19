#!/usr/bin/env python3
import os, sys

def validate_jwt_secret(project_path):
    env_path = os.path.join(project_path, ".env")
    if not os.path.exists(env_path):
        return False, f"{env_path} not found"
    with open(env_path) as f:
        for line in f:
            if line.startswith("JWT_SECRET="):
                secret = line.split("=", 1)[1].strip()
                if len(secret) < 32 or "change_me" in secret.lower():
                    return False, f"Invalid JWT_SECRET in {project_path}"
    return True, "OK"

if __name__ == "__main__":
    projects = ["cloudbudget", "infraflow", "netguardian", "netaegis"]
    for proj in projects:
        ok, msg = validate_jwt_secret(proj)
        print(f"{proj}: {msg}")
        if not ok:
            sys.exit(1)
