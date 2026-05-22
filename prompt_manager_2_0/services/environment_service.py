"""数据库环境配置管理逻辑。"""

from __future__ import annotations

from typing import Any

from prompt_manager_2_0.config.config_manager import (
    ConfigManager,
    EnvironmentConfig,
    get_config_path,
)
from prompt_manager_2_0.config.constants import ENV_TYPE_LABELS
from prompt_manager_2_0.db.mysql_connection import test_mysql_connection
from prompt_manager_2_0.repositories.local_status_repository import (
    LocalStatusRepository,
)
from prompt_manager_2_0.services.sync_service import SyncService
from prompt_manager_2_0.utils.db_utils import (
    build_db_identify,
    build_legacy_db_identify,
)


class EnvironmentService:
    """封装数据库环境配置的增删改查和连接校验。"""

    def __init__(self) -> None:
        self.config_manager = ConfigManager()
        self.sync_service = SyncService()
        self.local_status_repository = LocalStatusRepository()

    @property
    def config_path(self) -> str:
        return str(get_config_path())

    def list_environments(self) -> list[EnvironmentConfig]:
        return self.config_manager.list_environments()

    def get_environment(self, environment_id: str) -> EnvironmentConfig:
        return self.config_manager.get_environment(environment_id)

    def save_environment(self, data: dict[str, Any]) -> tuple[EnvironmentConfig, int]:
        self.validate_environment_data(data)
        self.validate_unique_database(data)
        previous_environment = self.find_existing_environment(data.get("id"))
        environment = EnvironmentConfig.from_dict(data)
        test_mysql_connection(environment)
        saved = self.config_manager.upsert_environment(environment.to_dict())
        if previous_environment and build_db_identify(
            previous_environment
        ) != build_db_identify(saved):
            self.delete_local_status_for_environment(previous_environment)
        synced_count = self.sync_service.sync_environment(saved)
        return saved, synced_count

    def test_environment_data(self, data: dict[str, Any]) -> None:
        self.validate_environment_data(data)
        environment = EnvironmentConfig.from_dict(data)
        test_mysql_connection(environment)

    def delete_environment(self, environment_id: str) -> EnvironmentConfig:
        environment = self.config_manager.delete_environment(environment_id)
        self.delete_local_status_for_environment(environment)
        return environment

    def delete_local_status_for_environment(
        self,
        environment: EnvironmentConfig,
    ) -> None:
        for db_identify in {
            build_db_identify(environment),
            build_legacy_db_identify(environment),
        }:
            self.local_status_repository.hard_delete_by_db_identify(db_identify)

    def test_and_sync(self, environment_id: str) -> int:
        environment = self.get_environment(environment_id)
        test_mysql_connection(environment)
        return self.sync_service.sync_environment(environment)

    def validate_environment_data(self, data: dict[str, Any]) -> None:
        if data.get("env_type") not in ENV_TYPE_LABELS:
            raise ValueError("环境类型只能选择开发环境、测试环境或预发布环境")
        for field, label in {
            "name": "环境名称",
            "host": "主机 IP",
            "port": "端口号",
            "user": "用户名",
            "database": "数据库名称",
        }.items():
            if data.get(field) in (None, ""):
                raise ValueError(f"{label}不能为空")
        port = int(data["port"])
        if port <= 0 or port > 65535:
            raise ValueError("端口号必须在 1 到 65535 之间")

    def validate_unique_database(self, data: dict[str, Any]) -> None:
        current_id = str(data.get("id") or "")
        target_key = self.database_key(data)
        for environment in self.list_environments():
            if environment.id == current_id:
                continue
            if self.database_key(environment.to_dict()) == target_key:
                raise ValueError("该数据库配置已存在，同一 IP:端口:数据库 只能添加一次")

    @staticmethod
    def database_key(data: dict[str, Any]) -> tuple[str, int, str]:
        return (
            str(data["host"]).strip().lower(),
            int(data["port"]),
            str(data["database"]).strip(),
        )

    def find_existing_environment(
        self,
        environment_id: Any,
    ) -> EnvironmentConfig | None:
        if not environment_id:
            return None
        for environment in self.list_environments():
            if environment.id == str(environment_id):
                return environment
        return None
