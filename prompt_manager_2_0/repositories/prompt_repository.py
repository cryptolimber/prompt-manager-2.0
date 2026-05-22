"""Prompt 数据访问逻辑。"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from typing import Any

from peewee import fn

from prompt_manager_2_0.config.config_manager import EnvironmentConfig
from prompt_manager_2_0.config.constants import (
    PROMPT_ALL_FIELDS,
    PROMPT_EDITABLE_FIELDS,
)
from prompt_manager_2_0.db.models.mysql_models import (
    AiagPromptTemplate,
    mysql_database_proxy,
)
from prompt_manager_2_0.db.mysql_connection import create_mysql_database
from prompt_manager_2_0.utils.time_utils import parse_datetime


class PromptRepository:
    """封装远程 aiag_prompt_template 表操作。"""

    def __init__(self, environment: EnvironmentConfig) -> None:
        self.environment = environment
        self.database = create_mysql_database(environment)

    @contextmanager
    def connection(self) -> Iterator[None]:
        mysql_database_proxy.initialize(self.database)
        try:
            self.database.connect(reuse_if_open=True)
            yield
        finally:
            if not self.database.is_closed():
                self.database.close()

    def count(self) -> int:
        with self.connection():
            return int(
                AiagPromptTemplate.select(fn.COUNT(AiagPromptTemplate.id))
                .where(self.not_deleted_condition())
                .scalar()
                or 0
            )

    def list_page(self, *, page: int, page_size: int) -> list[dict[str, Any]]:
        with self.connection():
            query = (
                AiagPromptTemplate.select()
                .where(self.not_deleted_condition())
                .order_by(AiagPromptTemplate.id.asc())
                .paginate(page, page_size)
            )
            return [self.to_dict(item) for item in query]

    def list_all(self) -> list[dict[str, Any]]:
        with self.connection():
            query = (
                AiagPromptTemplate.select()
                .where(self.not_deleted_condition())
                .order_by(AiagPromptTemplate.id.asc())
            )
            return [self.to_dict(item) for item in query]

    def get_by_id(self, prompt_id: int) -> dict[str, Any]:
        with self.connection():
            prompt = AiagPromptTemplate.get_by_id(prompt_id)
            return self.to_dict(prompt)

    def update_prompt(self, prompt_id: int, data: dict[str, Any]) -> int:
        cleaned = self.clean_update_data(data)
        if not cleaned:
            return 0
        with self.connection():
            current = AiagPromptTemplate.get_by_id(prompt_id)
            effective_code = cleaned.get("code", current.code)
            effective_status = cleaned.get("status", current.status)
            self.validate_active_code_unique(
                code=effective_code,
                status=effective_status,
                exclude_prompt_id=prompt_id,
            )
            return (
                AiagPromptTemplate.update(**cleaned)
                .where(AiagPromptTemplate.id == prompt_id)
                .execute()
            )

    def create_prompt(self, data: dict[str, Any]) -> dict[str, Any]:
        cleaned = self.clean_create_data(data)
        with self.connection():
            if "id" in cleaned:
                exists = (
                    AiagPromptTemplate.select(AiagPromptTemplate.id)
                    .where(AiagPromptTemplate.id == cleaned["id"])
                    .exists()
                )
                if exists:
                    raise ValueError("该 Prompt ID 已存在")
            self.validate_active_code_unique(
                code=cleaned.get("code"),
                status=cleaned.get("status"),
            )
            prompt = AiagPromptTemplate.create(**cleaned)
            prompt_id = prompt.id or self.database.execute_sql(
                "SELECT LAST_INSERT_ID()"
            ).fetchone()[0]
            created = AiagPromptTemplate.get_by_id(int(prompt_id))
            return self.to_dict(created)

    def mark_deleted(self, prompt_id: int) -> int:
        with self.connection():
            return (
                AiagPromptTemplate.update(status=0)
                .where(AiagPromptTemplate.id == prompt_id)
                .execute()
            )

    def upsert_prompt(self, prompt: dict[str, Any]) -> None:
        data = {
            field: prompt.get(field)
            for field in PROMPT_ALL_FIELDS
            if field in prompt
        }
        prompt_id = int(data["id"])
        with self.connection():
            exists = (
                AiagPromptTemplate.select(AiagPromptTemplate.id)
                .where(AiagPromptTemplate.id == prompt_id)
                .exists()
            )
            if exists:
                update_data = {
                    field: value
                    for field, value in data.items()
                    if field != "id"
                }
                self.validate_active_code_unique(
                    code=update_data.get("code"),
                    status=update_data.get("status"),
                    exclude_prompt_id=prompt_id,
                )
                (
                    AiagPromptTemplate.update(**update_data)
                    .where(AiagPromptTemplate.id == prompt_id)
                    .execute()
                )
            else:
                self.validate_active_code_unique(
                    code=data.get("code"),
                    status=data.get("status"),
                )
                AiagPromptTemplate.create(**data)

    def clean_update_data(self, data: dict[str, Any]) -> dict[str, Any]:
        cleaned: dict[str, Any] = {}
        for field in PROMPT_EDITABLE_FIELDS:
            if field not in data:
                continue
            value = data[field]
            if field in {"is_active", "status"}:
                cleaned[field] = None if value in (None, "") else int(value)
            elif field in {"tenant_id", "org_id"}:
                cleaned[field] = None if value in (None, "") else int(value)
            elif field == "create_time":
                cleaned[field] = parse_datetime(value)
            else:
                cleaned[field] = value
        return cleaned

    def clean_create_data(self, data: dict[str, Any]) -> dict[str, Any]:
        cleaned: dict[str, Any] = {}
        for field in PROMPT_ALL_FIELDS:
            value = data.get(field)
            if field == "id" and value in (None, ""):
                continue
            if field in {"id", "tenant_id", "org_id"}:
                cleaned[field] = None if value in (None, "") else int(value)
            elif field in {"is_active", "status"}:
                cleaned[field] = None if value in (None, "") else int(value)
            elif field == "create_time":
                cleaned[field] = parse_datetime(value)
            else:
                cleaned[field] = value
        return cleaned

    @staticmethod
    def is_not_deleted_status(status: Any) -> bool:
        return status != 0

    @staticmethod
    def not_deleted_condition():
        return (AiagPromptTemplate.status.is_null(True)) | (
            AiagPromptTemplate.status != 0
        )

    def validate_active_code_unique(
        self,
        *,
        code: Any,
        status: Any,
        exclude_prompt_id: int | None = None,
    ) -> None:
        if not self.is_not_deleted_status(status) or code in (None, ""):
            return

        query = AiagPromptTemplate.select(AiagPromptTemplate.id).where(
            self.not_deleted_condition(),
            AiagPromptTemplate.code == str(code),
        )
        if exclude_prompt_id is not None:
            query = query.where(AiagPromptTemplate.id != exclude_prompt_id)
        if query.exists():
            raise ValueError("非软删除 Prompt 中 code 必须唯一")

    @staticmethod
    def to_dict(prompt: AiagPromptTemplate) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for field in PROMPT_ALL_FIELDS:
            value = getattr(prompt, field)
            if isinstance(value, datetime):
                result[field] = value.replace(microsecond=0)
            else:
                result[field] = value
        return result
