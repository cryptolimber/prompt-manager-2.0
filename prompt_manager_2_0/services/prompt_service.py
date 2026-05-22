"""Prompt 查询、详情、编辑逻辑。"""

from __future__ import annotations

from typing import Any

from prompt_manager_2_0.config.config_manager import ConfigManager
from prompt_manager_2_0.config.constants import ENV_TYPE_DEV
from prompt_manager_2_0.repositories.local_status_repository import (
    LocalStatusRepository,
)
from prompt_manager_2_0.repositories.prompt_repository import PromptRepository
from prompt_manager_2_0.utils.db_utils import build_db_identify


class PromptService:
    def __init__(self) -> None:
        self.config_manager = ConfigManager()
        self.local_status_repository = LocalStatusRepository()

    def list_prompts(
        self,
        *,
        environment_id: str,
        page: int,
        page_size: int,
    ) -> tuple[list[dict[str, Any]], int]:
        environment = self.config_manager.get_environment(environment_id)
        repository = PromptRepository(environment)
        total = repository.count()
        rows = repository.list_page(page=page, page_size=page_size)
        last_modify_times = self.local_status_repository.get_last_modify_times(
            db_identify=build_db_identify(environment),
            prompt_ids=[int(row["id"]) for row in rows],
        )
        for row in rows:
            row["local_last_modify_time"] = last_modify_times.get(int(row["id"]))
        return rows, total

    def get_prompt(self, *, environment_id: str, prompt_id: int) -> dict[str, Any]:
        environment = self.config_manager.get_environment(environment_id)
        prompt = PromptRepository(environment).get_by_id(prompt_id)
        prompt["local_last_modify_time"] = (
            self.local_status_repository.get_last_modify_time(
                db_identify=build_db_identify(environment),
                prompt_id=prompt_id,
            )
        )
        return prompt

    def update_prompt(
        self,
        *,
        environment_id: str,
        prompt_id: int,
        data: dict[str, Any],
    ) -> None:
        environment = self.config_manager.get_environment(environment_id)
        self.ensure_development_environment(environment)
        repository = PromptRepository(environment)
        repository.update_prompt(prompt_id, data)
        prompt = repository.get_by_id(prompt_id)
        self.local_status_repository.upsert_many(
            db_identify=build_db_identify(environment),
            env_type=environment.env_type,
            prompts=[prompt],
        )

    def create_prompt(self, *, environment_id: str, data: dict[str, Any]) -> None:
        environment = self.config_manager.get_environment(environment_id)
        self.ensure_development_environment(environment)
        prompt = PromptRepository(environment).create_prompt(data)
        self.local_status_repository.upsert_many(
            db_identify=build_db_identify(environment),
            env_type=environment.env_type,
            prompts=[prompt],
        )

    def delete_prompt(self, *, environment_id: str, prompt_id: int) -> None:
        environment = self.config_manager.get_environment(environment_id)
        self.ensure_development_environment(environment)
        PromptRepository(environment).mark_deleted(prompt_id)
        self.local_status_repository.hard_delete_prompt_status(
            db_identify=build_db_identify(environment),
            prompt_id=prompt_id,
        )

    @staticmethod
    def ensure_development_environment(environment) -> None:
        if environment.env_type != ENV_TYPE_DEV:
            raise ValueError("只有开发环境允许新增、编辑或删除 Prompt")
