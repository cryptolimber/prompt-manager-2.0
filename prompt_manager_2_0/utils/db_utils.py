"""数据库辅助工具。"""

from __future__ import annotations

from prompt_manager_2_0.config.config_manager import EnvironmentConfig


def build_db_identify(environment: EnvironmentConfig) -> str:
    """生成远程数据库目标表唯一标识。"""

    host = environment.host.strip().lower()
    database = environment.database.strip()
    return f"{host}:{environment.port}:{database}"


def build_legacy_db_identify(environment: EnvironmentConfig) -> str:
    """返回早期版本使用的本地状态标识，用于删除旧数据。"""

    host = environment.host.strip().lower()
    return f"{host}:{environment.port}:aiag_prompt_template"
