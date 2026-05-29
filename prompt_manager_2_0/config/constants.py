"""项目常量定义。"""

from __future__ import annotations

APP_DATA_DIR_NAME = ".prompt_manager_2_0"
CONFIG_FILE_NAME = "PROMPT_MANAGER_CONFIG.json"
SQLITE_DB_FILE_NAME = "local_status.db"
PROMPT_TABLE_NAME = "aiag_prompt_template"

ENV_TYPE_DEV = "dev"
ENV_TYPE_TEST = "test"
ENV_TYPE_PRE_RELEASE = "pre_release"

ENV_TYPE_LABELS = {
    ENV_TYPE_DEV: "开发环境",
    ENV_TYPE_TEST: "测试环境",
    ENV_TYPE_PRE_RELEASE: "预发布环境",
}

ENV_TYPE_OPTIONS = [
    {"label": label, "value": value}
    for value, label in ENV_TYPE_LABELS.items()
]

PROMPT_DISPLAY_FIELDS = [
    "id",
    "code",
    "version",
    "description",
    "category",
    "is_active",
]

PROMPT_ALL_FIELDS = [
    "id",
    "prompt_content",
    "code",
    "version",
    "description",
    "category",
    "is_active",
    "tenant_id",
    "org_id",
    "create_time",
    "status",
]

PROMPT_EDITABLE_FIELDS = [
    "prompt_content",
    "code",
    "version",
    "description",
    "category",
    "is_active",
    "tenant_id",
    "org_id",
    "status",
]

PROMPT_READONLY_EDIT_FIELDS = [
    "create_time",
]
