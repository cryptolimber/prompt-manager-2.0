"""本地 SQLite 连接管理。"""

from __future__ import annotations

from pathlib import Path

from peewee import SqliteDatabase

from prompt_manager_2_0.config.constants import APP_DATA_DIR_NAME, SQLITE_DB_FILE_NAME


def get_sqlite_path() -> Path:
    """返回本地状态数据库路径。"""

    return Path.home() / APP_DATA_DIR_NAME / SQLITE_DB_FILE_NAME


sqlite_database = SqliteDatabase(
    get_sqlite_path(),
    timeout=10,
    pragmas={
        "journal_mode": "wal",
        "foreign_keys": 1,
        "busy_timeout": 10000,
    },
)


def initialize_sqlite_database() -> None:
    get_sqlite_path().parent.mkdir(parents=True, exist_ok=True)
