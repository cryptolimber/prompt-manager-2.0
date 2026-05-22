"""远程 MySQL 连接管理。"""

from __future__ import annotations

from peewee import MySQLDatabase

from prompt_manager_2_0.config.config_manager import EnvironmentConfig


def create_mysql_database(environment: EnvironmentConfig) -> MySQLDatabase:
    """按环境配置创建 MySQL 数据库实例。"""

    return MySQLDatabase(
        environment.database,
        user=environment.user,
        password=environment.password,
        host=environment.host,
        port=environment.port,
        charset="utf8mb4",
        connect_timeout=5,
    )


def test_mysql_connection(environment: EnvironmentConfig) -> None:
    """测试数据库是否可连接；失败时向上抛出 Peewee 或 PyMySQL 异常。"""

    database = create_mysql_database(environment)
    try:
        database.connect(reuse_if_open=True)
        database.execute_sql("SELECT 1")
    finally:
        if not database.is_closed():
            database.close()
