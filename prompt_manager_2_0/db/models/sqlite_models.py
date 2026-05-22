"""本地 SQLite 状态维护表模型。"""

from __future__ import annotations

from peewee import (
    AutoField,
    BigIntegerField,
    BooleanField,
    CharField,
    DateTimeField,
    Model,
)

from prompt_manager_2_0.db.sqlite_connection import sqlite_database


class BaseSqliteModel(Model):
    class Meta:
        database = sqlite_database


class AiagPromptLocalStatusMaintain(BaseSqliteModel):
    id = AutoField()
    remote_prompt_id = BigIntegerField(index=True)
    remote_create_time = DateTimeField(null=True)
    last_modify_time = DateTimeField(index=True)
    db_identify = CharField(max_length=255, index=True)
    env_type = CharField(max_length=50, index=True)
    is_deleted = BooleanField(default=False, column_name="delete")

    class Meta:
        table_name = "aiag_prompt_local_status_maintain_tb"
        indexes = (
            (("remote_prompt_id", "db_identify"), True),
        )


SQLITE_MODELS = [AiagPromptLocalStatusMaintain]
