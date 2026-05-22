"""开发环境推送到测试或预发布环境的逻辑。"""

from __future__ import annotations

from prompt_manager_2_0.config.config_manager import ConfigManager
from prompt_manager_2_0.config.constants import (
    ENV_TYPE_DEV,
    ENV_TYPE_PRE_RELEASE,
    ENV_TYPE_TEST,
)
from prompt_manager_2_0.repositories.local_status_repository import (
    LocalStatusRepository,
)
from prompt_manager_2_0.repositories.prompt_repository import PromptRepository
from prompt_manager_2_0.utils.db_utils import build_db_identify


class PublishService:
    def __init__(self) -> None:
        self.config_manager = ConfigManager()
        self.local_status_repository = LocalStatusRepository()

    def publish(
        self,
        *,
        source_environment_id: str,
        target_environment_id: str,
        prompt_ids: list[int],
    ) -> int:
        if not prompt_ids:
            raise ValueError("请选择需要推送的 Prompt 数据条目")

        source_environment = self.config_manager.get_environment(source_environment_id)
        target_environment = self.config_manager.get_environment(target_environment_id)

        if source_environment.env_type != ENV_TYPE_DEV:
            raise ValueError("只能从开发环境推送 Prompt")
        if target_environment.env_type not in {ENV_TYPE_TEST, ENV_TYPE_PRE_RELEASE}:
            raise ValueError("只能推送到测试环境或预发布环境")
        if build_db_identify(source_environment) == build_db_identify(
            target_environment
        ):
            raise ValueError("源环境和目标环境不能指向同一个数据库")

        source_repository = PromptRepository(source_environment)
        target_repository = PromptRepository(target_environment)

        published_prompts = []
        for prompt_id in prompt_ids:
            prompt = source_repository.get_by_id(prompt_id)
            if not PromptRepository.is_not_deleted_status(prompt.get("status")):
                raise ValueError(f"Prompt {prompt_id} 已软删除，不能推送")
            target_repository.upsert_prompt(prompt)
            published_prompts.append(prompt)

        self.local_status_repository.upsert_many(
            db_identify=build_db_identify(target_environment),
            env_type=target_environment.env_type,
            prompts=published_prompts,
        )
        return len(published_prompts)
