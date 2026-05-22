"""远程 Prompt 数据同步到本地 SQLite 的逻辑。"""

from __future__ import annotations

from prompt_manager_2_0.config.config_manager import EnvironmentConfig
from prompt_manager_2_0.repositories.local_status_repository import (
    LocalStatusRepository,
)
from prompt_manager_2_0.repositories.prompt_repository import PromptRepository
from prompt_manager_2_0.utils.db_utils import build_db_identify


class SyncService:
    def __init__(self) -> None:
        self.local_status_repository = LocalStatusRepository()

    def sync_environment(self, environment: EnvironmentConfig) -> int:
        prompts = PromptRepository(environment).list_all()
        return self.local_status_repository.upsert_many(
            db_identify=build_db_identify(environment),
            env_type=environment.env_type,
            prompts=prompts,
        )
