"""Prompt 管理页面。"""

from __future__ import annotations

from math import ceil
from typing import Any

from nicegui import ui

from prompt_manager_2_0.config.constants import (
    DEFAULT_PAGE_SIZE,
    ENV_TYPE_DEV,
    ENV_TYPE_PRE_RELEASE,
    ENV_TYPE_TEST,
    PAGE_SIZE_OPTIONS,
    PROMPT_ALL_FIELDS,
    PROMPT_DISPLAY_FIELDS,
    PROMPT_EDITABLE_FIELDS,
    PROMPT_READONLY_EDIT_FIELDS,
)
from prompt_manager_2_0.services.environment_service import EnvironmentService
from prompt_manager_2_0.services.prompt_service import PromptService
from prompt_manager_2_0.services.publish_service import PublishService
from prompt_manager_2_0.ui.components import (
    environment_select_options,
    format_prompt_row,
    notify_error,
    notify_success,
    prompt_detail_rows,
)
from prompt_manager_2_0.utils.time_utils import format_datetime, now


def add_prompt_table_styles() -> None:
    ui.add_head_html(
        """
        <style>
        .prompt-table-scroll {
            width: 100%;
            max-width: 100%;
            height: min(500px, calc(100vh - 285px));
            min-height: 340px;
            overflow: auto;
        }

        .prompt-table {
            width: 100%;
            min-width: 1320px;
        }

        .prompt-table .q-table th,
        .prompt-table .q-table td {
            text-align: left;
            white-space: nowrap;
        }

        .prompt-table .q-table thead tr th:first-child,
        .prompt-table .q-table tbody tr td:first-child {
            position: sticky;
            left: 0;
            z-index: 3;
            width: 48px;
            min-width: 48px;
            max-width: 48px;
            background: #fff;
        }

        .prompt-table .q-table thead tr th:nth-child(2),
        .prompt-table .q-table tbody tr td:nth-child(2) {
            position: sticky;
            left: 48px;
            z-index: 3;
            width: 72px;
            min-width: 72px;
            max-width: 72px;
            background: #fff;
            box-shadow: 1px 0 0 rgba(0, 0, 0, 0.08);
        }

        .prompt-table .q-table thead tr th:last-child,
        .prompt-table .q-table tbody tr td:last-child {
            position: sticky;
            right: 0;
            z-index: 3;
            width: 148px;
            min-width: 148px;
            max-width: 148px;
            background: #fff;
            box-shadow: -1px 0 0 rgba(0, 0, 0, 0.08);
        }

        .prompt-row-actions {
            display: flex;
            flex-wrap: nowrap;
            justify-content: flex-start;
            align-items: center;
            gap: 2px;
            min-width: 124px;
        }

        .prompt-table .q-table thead tr th:first-child,
        .prompt-table .q-table thead tr th:nth-child(2),
        .prompt-table .q-table thead tr th:last-child {
            z-index: 4;
            background: #fff;
        }

        .prompt-table .q-table tbody tr:hover td:first-child,
        .prompt-table .q-table tbody tr:hover td:nth-child(2),
        .prompt-table .q-table tbody tr:hover td:last-child {
            background: #f5f5f5;
        }

        .prompt-edit-card {
            max-height: 86vh;
            overflow-y: auto;
        }

        .prompt-content-editor textarea {
            min-height: 96px;
            resize: vertical;
        }
        </style>
        """
    )


def create_prompt_manage_page() -> None:
    add_prompt_table_styles()
    environment_service = EnvironmentService()
    prompt_service = PromptService()
    publish_service = PublishService()
    environments = environment_service.list_environments()
    options = environment_select_options(environments)

    state: dict[str, Any] = {
        "environment_id": next(iter(options), None),
        "target_environment_id": None,
        "page": 1,
        "page_size": DEFAULT_PAGE_SIZE,
        "total": 0,
        "selected_ids": [],
    }
    table_holder: dict[str, Any] = {}
    operation_controls: list[Any] = []

    def get_current_environment():
        if not state["environment_id"]:
            return None
        try:
            return environment_service.get_environment(state["environment_id"])
        except Exception:
            return None

    def current_environment_can_modify() -> bool:
        environment = get_current_environment()
        return bool(environment and environment.env_type == ENV_TYPE_DEV)

    def update_operation_controls() -> None:
        can_modify = current_environment_can_modify()
        for control in operation_controls:
            control.visible = can_modify
            control.update()

    def load_rows() -> None:
        table = table_holder.get("table")
        if table is None:
            return
        if not state["environment_id"]:
            table.rows = []
            table.update()
            update_operation_controls()
            total_label.set_text("共 0 条")
            page_label.set_text("第 1 / 1 页")
            return
        try:
            rows, total = prompt_service.list_prompts(
                environment_id=state["environment_id"],
                page=state["page"],
                page_size=state["page_size"],
            )
        except Exception as error:
            notify_error(error)
            return
        state["total"] = total
        state["selected_ids"] = []
        sequence_start = (state["page"] - 1) * state["page_size"] + 1
        can_modify = current_environment_can_modify()
        table.rows = [
            format_prompt_row(
                row,
                sequence=sequence_start + index,
                can_modify=can_modify,
            )
            for index, row in enumerate(rows)
        ]
        table.update()
        update_operation_controls()
        total_pages = max(1, ceil(total / state["page_size"]))
        page_label.set_text(f"第 {state['page']} / {total_pages} 页")
        total_label.set_text(f"共 {total} 条")

    def refresh_environment_options() -> None:
        fresh_environments = environment_service.list_environments()
        fresh_options = environment_select_options(fresh_environments)
        env_select.options = fresh_options
        if state["environment_id"] not in fresh_options:
            state["environment_id"] = next(iter(fresh_options), None)
            env_select.value = state["environment_id"]
        env_select.update()
        load_rows()

    def on_environment_change(event) -> None:
        state["environment_id"] = event.value
        state["page"] = 1
        load_rows()

    def on_page_size_change(event) -> None:
        state["page_size"] = int(event.value)
        state["page"] = 1
        load_rows()

    def on_select(event) -> None:
        state["selected_ids"] = [int(row["id"]) for row in event.selection]

    def previous_page() -> None:
        if state["page"] <= 1:
            return
        state["page"] -= 1
        load_rows()

    def next_page() -> None:
        total_pages = max(1, ceil(state["total"] / state["page_size"]))
        if state["page"] >= total_pages:
            return
        state["page"] += 1
        load_rows()

    def show_detail(prompt_id: int) -> None:
        try:
            prompt = prompt_service.get_prompt(
                environment_id=state["environment_id"],
                prompt_id=prompt_id,
            )
        except Exception as error:
            notify_error(error)
            return
        with ui.dialog() as dialog, ui.card().classes("w-[720px] max-w-full"):
            ui.label("Prompt 详情").classes("text-lg font-medium")
            for field, value in prompt_detail_rows(prompt):
                with ui.row().classes("w-full items-start"):
                    ui.label(field).classes("w-32 text-gray-600")
                    if field == "code":
                        ui.label(value).classes("flex-1 whitespace-pre-wrap")
                        ui.button(
                            "复制",
                            icon="content_copy",
                            on_click=lambda code=value: copy_prompt_code(code),
                        ).props("outline dense")
                    else:
                        ui.label(value).classes("flex-1 whitespace-pre-wrap")
            with ui.row().classes("justify-end w-full"):
                ui.button("关闭", icon="close", on_click=dialog.close)
        dialog.open()

    def copy_prompt_code(code: str) -> None:
        ui.clipboard.write(code)
        notify_success("code 已复制")

    def show_create_prompt() -> None:
        if not state["environment_id"]:
            notify_error("请先选择数据库环境")
            return
        if not current_environment_can_modify():
            notify_error("只有开发环境允许新增 Prompt")
            return

        inputs: dict[str, Any] = {}
        defaults = {
            "create_time": format_datetime(now()),
            "is_active": 1,
            "status": 1,
        }

        with ui.dialog() as dialog, ui.card().classes(
            "prompt-edit-card w-[760px] max-w-full"
        ):
            ui.label("新增 PROMPT").classes("text-lg font-medium")
            for field in [field for field in PROMPT_ALL_FIELDS if field != "id"]:
                if field == "prompt_content":
                    inputs[field] = ui.textarea(field, value="").classes(
                        "prompt-content-editor w-full"
                    ).props("rows=4")
                elif field in {"id", "is_active", "tenant_id", "org_id", "status"}:
                    inputs[field] = ui.number(
                        field,
                        value=defaults.get(field),
                    ).classes("w-full")
                elif field == "create_time":
                    value = defaults.get(field, "")
                    inputs[field] = ui.input(field, value=value).classes(
                        "w-full"
                    ).props("disable")
                else:
                    inputs[field] = ui.input(field, value="").classes("w-full")

            def save() -> None:
                try:
                    prompt_service.create_prompt(
                        environment_id=state["environment_id"],
                        data={field: element.value for field, element in inputs.items()},
                    )
                except Exception as error:
                    notify_error(error)
                    return
                notify_success("PROMPT 已新增")
                state["page"] = 1
                dialog.close()
                load_rows()

            with ui.row().classes("justify-end w-full"):
                ui.button("取消", icon="close", on_click=dialog.close).props("flat")
                ui.button("保存", icon="save", on_click=save)
        dialog.open()

    def show_editor(prompt_id: int) -> None:
        if not current_environment_can_modify():
            notify_error("只有开发环境允许编辑 Prompt")
            return
        try:
            prompt = prompt_service.get_prompt(
                environment_id=state["environment_id"],
                prompt_id=prompt_id,
            )
        except Exception as error:
            notify_error(error)
            return

        inputs: dict[str, Any] = {}
        with ui.dialog() as dialog, ui.card().classes(
            "prompt-edit-card w-[760px] max-w-full"
        ):
            ui.label(f"编辑 Prompt：{prompt_id}").classes("text-lg font-medium")
            for field in [field for field in PROMPT_ALL_FIELDS if field != "id"]:
                value = format_datetime(prompt.get(field))
                if field == "prompt_content":
                    inputs[field] = ui.textarea(field, value=value).classes(
                        "prompt-content-editor w-full"
                    ).props("rows=4")
                elif field in {"is_active", "tenant_id", "org_id", "status"}:
                    inputs[field] = ui.number(field, value=prompt.get(field)).classes(
                        "w-full"
                    )
                elif field in PROMPT_READONLY_EDIT_FIELDS:
                    inputs[field] = ui.input(field, value=value).classes(
                        "w-full"
                    ).props("disable")
                else:
                    inputs[field] = ui.input(field, value=value).classes("w-full")

            def save() -> None:
                try:
                    prompt_service.update_prompt(
                        environment_id=state["environment_id"],
                        prompt_id=prompt_id,
                        data={
                            field: inputs[field].value
                            for field in PROMPT_EDITABLE_FIELDS
                        },
                    )
                except Exception as error:
                    notify_error(error)
                    return
                notify_success("Prompt 已保存")
                dialog.close()
                load_rows()

            with ui.row().classes("justify-end w-full"):
                ui.button("取消", icon="close", on_click=dialog.close).props("flat")
                ui.button("保存", icon="save", on_click=save)
        dialog.open()

    def delete_prompt(prompt_id: int) -> None:
        if not current_environment_can_modify():
            notify_error("只有开发环境允许删除 Prompt")
            return
        with ui.dialog() as dialog, ui.card():
            ui.label(f"确认删除 Prompt：{prompt_id}")
            ui.label("远程记录会标记 status=0，本地状态记录会硬删除。").classes(
                "text-sm text-gray-600"
            )

            def confirm() -> None:
                try:
                    prompt_service.delete_prompt(
                        environment_id=state["environment_id"],
                        prompt_id=prompt_id,
                    )
                except Exception as error:
                    notify_error(error)
                    return
                notify_success("Prompt 已删除")
                dialog.close()
                load_rows()

            with ui.row().classes("justify-end w-full"):
                ui.button("取消", icon="close", on_click=dialog.close).props("flat")
                ui.button("删除", icon="delete", on_click=confirm).props("color=negative")
        dialog.open()

    def handle_action(event) -> None:
        action = event.args.get("action")
        prompt_id = int(event.args["id"])
        if action == "detail":
            show_detail(prompt_id)
        elif action == "edit":
            show_editor(prompt_id)
        elif action == "delete":
            delete_prompt(prompt_id)

    def publish_selected() -> None:
        if not current_environment_can_modify():
            notify_error("只能从开发环境推送 Prompt")
            return
        if not state["selected_ids"]:
            notify_error("请先选择需要推送的数据条目")
            return

        fresh_environments = environment_service.list_environments()
        target_options = environment_select_options(
            fresh_environments,
            env_types={ENV_TYPE_TEST, ENV_TYPE_PRE_RELEASE},
        )
        if not target_options:
            notify_error("请先配置测试环境或预发布环境")
            return

        with ui.dialog() as dialog, ui.card().classes("w-[480px] max-w-full"):
            ui.label("推送目标环境").classes("text-lg font-medium")
            ui.label(f"已选择 {len(state['selected_ids'])} 条数据条目").classes(
                "text-sm text-gray-600"
            )
            dialog_target_select = ui.select(
                target_options,
                label="目标环境",
                value=next(iter(target_options), None),
            ).classes("w-full")

            def confirm_publish() -> None:
                if not dialog_target_select.value:
                    notify_error("请选择推送目标环境")
                    return
                try:
                    count = publish_service.publish(
                        source_environment_id=state["environment_id"],
                        target_environment_id=dialog_target_select.value,
                        prompt_ids=state["selected_ids"],
                    )
                except Exception as error:
                    notify_error(error)
                    return
                notify_success(f"已推送 {count} 条 Prompt 数据")
                dialog.close()

            with ui.row().classes("justify-end w-full"):
                ui.button("取消", icon="close", on_click=dialog.close).props("flat")
                ui.button("推送", icon="upload", on_click=confirm_publish)
        dialog.open()

    columns = [
        {
            "name": "sequence",
            "label": "序号",
            "field": "sequence",
            "align": "left",
            "sortable": False,
        },
    ]
    for field in PROMPT_DISPLAY_FIELDS:
        columns.append(
            {
                "name": field,
                "label": field,
                "field": field,
                "align": "left",
                "sortable": True,
            }
        )
        if field == "is_active":
            columns.append(
                {
                    "name": "local_last_modify_time",
                    "label": "最近更新时间",
                    "field": "local_last_modify_time",
                    "align": "left",
                    "sortable": True,
                }
            )
    columns.append(
        {
            "name": "action",
            "label": "操作",
            "field": "action",
            "align": "left",
        }
    )

    ui.label("Prompt 管理").classes("text-lg font-semibold")
    with ui.row().classes("items-center gap-2 w-full"):
        env_select = ui.select(
            options,
            label="数据库环境",
            value=state["environment_id"],
            on_change=on_environment_change,
        ).classes("min-w-72")
        ui.button("刷新环境", icon="refresh", on_click=refresh_environment_options).props("outline")
        ui.button("查询", icon="search", on_click=load_rows)
        create_button = ui.button(
            "新增 PROMPT",
            icon="add",
            on_click=show_create_prompt,
        ).props("outline")
        operation_controls.append(create_button)
        ui.space()
        publish_button = ui.button(
            "推送选中",
            icon="upload",
            on_click=publish_selected,
        ).props("outline")
        operation_controls.append(publish_button)

    with ui.element("div").classes(
        "prompt-table-scroll border border-gray-200 rounded"
    ):
        table = ui.table(
            columns=columns,
            rows=[],
            row_key="id",
            selection="multiple",
            on_select=on_select,
            pagination={"rowsPerPage": 0},
        ).classes("prompt-table").props("hide-pagination dense")
    table_holder["table"] = table
    with table.add_slot("body-cell-action"):
        with table.cell("action"):
            with ui.element("div").classes("prompt-row-actions"):
                ui.button(icon="visibility").props("flat dense round").tooltip("详情").on(
                    "click",
                    js_handler='() => emit({"action": "detail", "id": props.row.id})',
                    handler=handle_action,
                )
                edit_button = ui.button(icon="edit").props(
                    'flat dense round :disable="!props.row.can_modify"'
                )
                edit_button.tooltip("编辑").on(
                    "click",
                    js_handler='() => emit({"action": "edit", "id": props.row.id})',
                    handler=handle_action,
                )
                delete_button = ui.button(icon="delete").props(
                    'flat dense round color=negative :disable="!props.row.can_modify"'
                )
                delete_button.tooltip("删除").on(
                    "click",
                    js_handler='() => emit({"action": "delete", "id": props.row.id})',
                    handler=handle_action,
                )

    with ui.row().classes("items-center w-full gap-2"):
        page_size_select = ui.select(
            PAGE_SIZE_OPTIONS,
            label="每页数量",
            value=state["page_size"],
            on_change=on_page_size_change,
        ).classes("w-32")
        ui.space()
        total_label = ui.label("共 0 条")
        page_label = ui.label("第 1 / 1 页")
        ui.button(icon="chevron_left", on_click=previous_page).tooltip("上一页")
        ui.button(icon="chevron_right", on_click=next_page).tooltip("下一页")

    load_rows()
