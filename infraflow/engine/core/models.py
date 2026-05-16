from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class Action(BaseModel):
    type: str
    condition: str = 'True'
    priority: Literal['info', 'warning', 'high', 'critical'] = 'info'
    target: str | None = None
    path: str | None = None
    message: str | None = None
    playbook: str | None = None


class Check(BaseModel):
    type: Literal['cpu', 'memory', 'disk', 'service', 'port', 'ansible_playbook']
    threshold: float | None = None
    path: str | None = None
    name: str | None = None
    port: int | None = None
    actions: list[Action] = Field(default_factory=list)


class ServerConfig(BaseModel):
    name: str
    host: str
    user: str
    key_file: str | None = None
    tags: list[str] = Field(default_factory=list)
    alerting: dict[str, Any] = Field(default_factory=dict)
    checks: list[Check] = Field(default_factory=list)


class ConfigModel(BaseModel):
    global_: dict[str, Any] = Field(default_factory=dict, alias='global')
    servers: list[ServerConfig] = Field(default_factory=list)
