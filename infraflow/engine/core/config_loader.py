from __future__ import annotations

import os

import yaml

from core.models import ConfigModel

CONFIG_PATH = os.getenv('CONFIG_PATH', '/app/config/servers.yml')


def load_config() -> dict:
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    # validate shape
    ConfigModel.model_validate(data)
    return data
