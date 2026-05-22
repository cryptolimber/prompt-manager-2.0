"""远程 MySQL 表模型。"""

from __future__ import annotations

from peewee import (
    BigIntegerField,
    CharField,
    DatabaseProxy,
    DateTimeField,
    IntegerField,
    Model,
    TextField,
)

from prompt_manager_2_0.config.constants import PROMPT_TABLE_NAME

mysql_database_proxy = DatabaseProxy()


class BaseMysqlModel(Model):
    class Meta:
        database = mysql_database_proxy


class AiagPromptTemplate(BaseMysqlModel):
    id = BigIntegerField(primary_key=True)
    prompt_content = TextField(null=True)
    code = CharField(max_length=100, null=True)
    version = CharField(max_length=50, null=True)
    description = CharField(max_length=1024, null=True)
    category = CharField(max_length=50, null=True)
    is_active = IntegerField(null=True)
    tenant_id = BigIntegerField(null=True)
    org_id = BigIntegerField(null=True)
    create_time = DateTimeField(null=True)
    status = IntegerField(null=True)

    class Meta:
        table_name = PROMPT_TABLE_NAME

