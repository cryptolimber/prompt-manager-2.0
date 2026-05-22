"""本地配置文件读写逻辑。"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from prompt_manager_2_0.config.constants import CONFIG_FILE_NAME, ENV_TYPE_LABELS


@dataclass(slots=True)
class EnvironmentConfig:
    """远程数据库环境配置。"""

    id: str
    env_type: str
    name: str
    host: str
    port: int
    user: str
    password: str
    database: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EnvironmentConfig":
        return cls(
            id=str(data.get("id") or uuid.uuid4()),
            env_type=str(data["env_type"]),
            name=str(data["name"]),
            host=str(data["host"]),
            port=int(data["port"]),
            user=str(data["user"]),
            password=str(data.get("password", "")),
            database=str(data["database"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "env_type": self.env_type,
            "name": self.name,
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database,
        }

    @property
    def env_label(self) -> str:
        return ENV_TYPE_LABELS.get(self.env_type, self.env_type)

    @property
    def display_name(self) -> str:
        return f"{self.env_label} - {self.name}"


@dataclass(slots=True)
class AppConfig:
    environments: list[EnvironmentConfig] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AppConfig":
        environments = [
            EnvironmentConfig.from_dict(item)
            for item in data.get("environments", [])
        ]
        return cls(environments=environments)

    def to_dict(self) -> dict[str, Any]:
        return {
            "environments": [
                environment.to_dict()
                for environment in self.environments
            ]
        }


def get_config_path() -> Path:
    """返回用户目录下的默认配置文件路径。"""

    return Path.home() / CONFIG_FILE_NAME


class ConfigManager:
    """负责持久化数据库环境配置。"""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or get_config_path()

    def load(self) -> AppConfig:
        if not self.path.exists():
            return AppConfig()
        with self.path.open("r", encoding="utf-8") as file:
            raw = json.load(file)
        return AppConfig.from_dict(raw)

    def save(self, config: AppConfig) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix(".tmp")
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(config.to_dict(), file, ensure_ascii=False, indent=2)
        temp_path.replace(self.path)

    def list_environments(self) -> list[EnvironmentConfig]:
        return self.load().environments

    def get_environment(self, environment_id: str) -> EnvironmentConfig:
        for environment in self.list_environments():
            if environment.id == environment_id:
                return environment
        raise ValueError("未找到数据库环境配置")

    def upsert_environment(self, data: dict[str, Any]) -> EnvironmentConfig:
        config = self.load()
        environment = EnvironmentConfig.from_dict(
            {
                **data,
                "id": data.get("id") or str(uuid.uuid4()),
            }
        )

        for index, existing in enumerate(config.environments):
            if existing.id == environment.id:
                config.environments[index] = environment
                self.save(config)
                return environment

        config.environments.append(environment)
        self.save(config)
        return environment

    def delete_environment(self, environment_id: str) -> EnvironmentConfig:
        config = self.load()
        removed: EnvironmentConfig | None = None
        remaining: list[EnvironmentConfig] = []
        for environment in config.environments:
            if environment.id == environment_id:
                removed = environment
            else:
                remaining.append(environment)
        if removed is None:
            raise ValueError("未找到数据库环境配置")
        config.environments = remaining
        self.save(config)
        return removed
