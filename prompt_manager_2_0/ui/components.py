"""通用 UI 组件。"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from nicegui import ui

from prompt_manager_2_0.config.config_manager import EnvironmentConfig
from prompt_manager_2_0.config.constants import (
    ENV_TYPE_LABELS,
    PROMPT_ALL_FIELDS,
    PROMPT_DISPLAY_FIELDS,
)
from prompt_manager_2_0.utils.time_utils import format_datetime


def environment_type_options() -> dict[str, str]:
    return dict(ENV_TYPE_LABELS)


def environment_select_options(
    environments: Iterable[EnvironmentConfig],
    *,
    env_types: set[str] | None = None,
) -> dict[str, str]:
    options: dict[str, str] = {}
    for environment in environments:
        if env_types is not None and environment.env_type not in env_types:
            continue
        options[environment.id] = environment.display_name
    return options


def notify_success(message: str) -> None:
    ui.notify(message, type="positive", position="top")


def notify_error(error: Exception | str) -> None:
    ui.notify(str(error), type="negative", position="top")


def truncate_text(value: Any, max_length: int = 15) -> str:
    text = "" if value is None else str(value)
    if len(text) <= max_length:
        return text
    return f"{text[:max_length]}..."


def format_prompt_row(
    prompt: dict[str, Any],
    *,
    sequence: int,
    can_modify: bool = False,
) -> dict[str, Any]:
    row = {field: prompt.get(field) for field in PROMPT_DISPLAY_FIELDS}
    row["sequence"] = sequence
    row["description"] = truncate_text(prompt.get("description"))
    row["local_last_modify_time"] = (
        format_datetime(prompt.get("local_last_modify_time")) or "无更新"
    )
    row["can_modify"] = can_modify
    row["action"] = ""
    return row


def prompt_detail_rows(prompt: dict[str, Any]) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for field in PROMPT_ALL_FIELDS:
        value = prompt.get(field)
        rows.append((field, format_datetime(value)))
    rows.append(
        (
            "最近更新时间",
            format_datetime(prompt.get("local_last_modify_time")) or "无更新",
        )
    )
    return rows
