#!/usr/bin/env python3
import argparse
import os
import re
import sys
from pathlib import Path

import yaml

JWT_PATTERN = re.compile(r"^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]{32,}$")


def parse_env(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        raise FileNotFoundError(f"Missing env file: {path}")
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        data[k.strip()] = v.strip()
    return data


def validate_ports(services: dict) -> None:
    seen = {}
    for name, cfg in services.items():
        for port in cfg.get("ports", []):
            if port in seen:
                raise ValueError(f"Duplicate port {port} found in {name} and {seen[port]}")
            seen[port] = name


def validate(config: dict, environment: str) -> None:
    if environment not in config.get("environments", {}):
        raise ValueError(f"Unknown environment override: {environment}")

    services = config["services"]
    validate_ports(services)
    shared = config.get("shared_required", [])

    for name, cfg in services.items():
        env = parse_env(Path(cfg["env_file"]))
        missing = [var for var in shared if var not in env]
        if missing:
            raise ValueError(f"{name} missing required vars: {', '.join(missing)}")
        if cfg.get("jwt_required"):
            jwt = env.get("JWT_SECRET", "")
            if not JWT_PATTERN.match(jwt):
                raise ValueError(f"{name} has invalid JWT_SECRET format")


def generate_env_examples(config: dict) -> None:
    for name, cfg in config["services"].items():
        out = Path(name) / ".env.example"
        lines = ["ENVIRONMENT=dev", "LOG_LEVEL=INFO"]
        if cfg.get("jwt_required"):
            lines.append("JWT_SECRET=replace_with_a_strong_secret_at_least_32_chars")
        lines.append(f"SERVICE_PORT={cfg['ports'][0]}")
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_compose_env(config: dict, environment: str) -> None:
    out = Path("config") / f"docker-compose.{environment}.env"
    rows = [f"ENVIRONMENT={environment}"]
    for name, cfg in config["services"].items():
        rows.append(f"{name.upper()}_PORT={cfg['ports'][0]}")
    out.write_text("\n".join(rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/services.yml")
    parser.add_argument("--environment", default="dev")
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    validate(cfg, args.environment)
    if args.generate:
        generate_env_examples(cfg)
        generate_compose_env(cfg, args.environment)
    print("Configuration validation successful")
