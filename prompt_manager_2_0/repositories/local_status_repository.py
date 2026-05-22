"""本地状态维护表数据访问逻辑。"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

from peewee import IntegrityError

from prompt_manager_2_0.db.models.sqlite_models import (
    AiagPromptLocalStatusMaintain,
    SQLITE_MODELS,
)
from prompt_manager_2_0.db.sqlite_connection import (
    initialize_sqlite_database,
    sqlite_database,
)
from prompt_manager_2_0.utils.time_utils import now


class LocalStatusRepository:
    """封装本地 SQLite 状态表操作。"""

    def initialize(self) -> None:
        initialize_sqlite_database()
        with sqlite_database.connection_context():
            sqlite_database.create_tables(SQLITE_MODELS, safe=True)

    def upsert_many(
        self,
        *,
        db_identify: str,
        env_type: str,
        prompts: Iterable[dict],
        modify_time: datetime | None = None,
    ) -> int:
        self.initialize()
        current_time = modify_time or now()
        count = 0
        with sqlite_database.connection_context():
            with sqlite_database.atomic():
                for prompt in prompts:
                    defaults = {
                        "remote_create_time": prompt.get("create_time"),
                        "last_modify_time": current_time,
                        "env_type": env_type,
                        "is_deleted": False,
                    }
                    try:
                        AiagPromptLocalStatusMaintain.create(
                            remote_prompt_id=prompt["id"],
                            db_identify=db_identify,
                            **defaults,
                        )
                    except IntegrityError:
                        (
                            AiagPromptLocalStatusMaintain.update(**defaults)
                            .where(
                                AiagPromptLocalStatusMaintain.remote_prompt_id
                                == prompt["id"],
                                AiagPromptLocalStatusMaintain.db_identify
                                == db_identify,
                            )
                            .execute()
                        )
                    count += 1
        return count

    def hard_delete_by_db_identify(self, db_identify: str) -> int:
        self.initialize()
        with sqlite_database.connection_context():
            return (
                AiagPromptLocalStatusMaintain.delete()
                .where(AiagPromptLocalStatusMaintain.db_identify == db_identify)
                .execute()
            )

    def hard_delete_prompt_status(self, *, db_identify: str, prompt_id: int) -> int:
        self.initialize()
        with sqlite_database.connection_context():
            return (
                AiagPromptLocalStatusMaintain.delete()
                .where(
                    AiagPromptLocalStatusMaintain.db_identify == db_identify,
                    AiagPromptLocalStatusMaintain.remote_prompt_id == prompt_id,
                )
                .execute()
            )

    def mark_prompt_modified(self, *, db_identify: str, prompt_id: int) -> int:
        self.initialize()
        with sqlite_database.connection_context():
            return (
                AiagPromptLocalStatusMaintain.update(
                    last_modify_time=now(),
                    is_deleted=False,
                )
                .where(
                    AiagPromptLocalStatusMaintain.db_identify == db_identify,
                    AiagPromptLocalStatusMaintain.remote_prompt_id == prompt_id,
                )
                .execute()
            )

    def get_last_modify_time(
        self,
        *,
        db_identify: str,
        prompt_id: int,
    ) -> datetime | None:
        self.initialize()
        with sqlite_database.connection_context():
            record = (
                AiagPromptLocalStatusMaintain.select(
                    AiagPromptLocalStatusMaintain.last_modify_time
                )
                .where(
                    AiagPromptLocalStatusMaintain.db_identify == db_identify,
                    AiagPromptLocalStatusMaintain.remote_prompt_id == prompt_id,
                    AiagPromptLocalStatusMaintain.is_deleted == False,  # noqa: E712
                )
                .first()
            )
            return record.last_modify_time if record else None

    def get_last_modify_times(
        self,
        *,
        db_identify: str,
        prompt_ids: Iterable[int],
    ) -> dict[int, datetime]:
        ids = [int(prompt_id) for prompt_id in prompt_ids]
        if not ids:
            return {}

        self.initialize()
        with sqlite_database.connection_context():
            records = (
                AiagPromptLocalStatusMaintain.select(
                    AiagPromptLocalStatusMaintain.remote_prompt_id,
                    AiagPromptLocalStatusMaintain.last_modify_time,
                )
                .where(
                    AiagPromptLocalStatusMaintain.db_identify == db_identify,
                    AiagPromptLocalStatusMaintain.remote_prompt_id.in_(ids),
                    AiagPromptLocalStatusMaintain.is_deleted == False,  # noqa: E712
                )
            )
            return {
                int(record.remote_prompt_id): record.last_modify_time
                for record in records
            }
