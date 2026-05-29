"""数据库环境配置页面。"""

from __future__ import annotations

from nicegui import ui

from prompt_manager_2_0.config.config_manager import EnvironmentConfig
from prompt_manager_2_0.services.environment_service import EnvironmentService
from prompt_manager_2_0.ui.components import (
    environment_type_options,
    notify_error,
    notify_success,
)


def create_environment_page() -> None:
    service = EnvironmentService()

    @ui.refreshable
    def environment_table() -> None:
        environments = service.list_environments()
        rows = [
            {
                "id": environment.id,
                "env_type": environment.env_label,
                "name": environment.name,
                "host": environment.host,
                "port": environment.port,
                "database": environment.database,
                "user": environment.user,
                "action": "",
            }
            for environment in environments
        ]

        with ui.element("div").classes(
            "w-full h-[520px] overflow-auto border border-gray-200 rounded"
        ):
            table = ui.table(
                columns=[
                    {"name": "env_type", "label": "环境类型", "field": "env_type"},
                    {"name": "name", "label": "环境名称", "field": "name"},
                    {"name": "host", "label": "主机 IP", "field": "host"},
                    {"name": "port", "label": "端口号", "field": "port"},
                    {"name": "database", "label": "数据库名称", "field": "database"},
                    {"name": "user", "label": "用户名", "field": "user"},
                    {"name": "action", "label": "操作", "field": "action"},
                ],
                rows=rows,
                row_key="id",
                pagination={"rowsPerPage": 0},
            ).classes("w-full min-w-[900px]").props("hide-pagination")

        with table.add_slot("body-cell-action"):
            with table.cell("action"):
                with ui.row().classes("gap-1 justify-end no-wrap"):
                    ui.button("编辑").props("flat dense").on(
                        "click",
                        js_handler='() => emit({"action": "edit", "id": props.row.id})',
                        handler=handle_action,
                    )
                    ui.button("同步").props("flat dense").on(
                        "click",
                        js_handler='() => emit({"action": "sync", "id": props.row.id})',
                        handler=handle_action,
                    )
                    ui.button("删除").props("flat dense color=negative").on(
                        "click",
                        js_handler='() => emit({"action": "delete", "id": props.row.id})',
                        handler=handle_action,
                    )

    def open_editor(environment: EnvironmentConfig | None = None) -> None:
        with ui.dialog() as dialog, ui.card().classes("w-[560px] max-w-full"):
            ui.label("数据库环境").classes("text-lg font-medium")
            env_type = ui.select(
                environment_type_options(),
                label="环境类型",
                value=environment.env_type if environment else "dev",
            ).classes("w-full")
            name = ui.input(
                "环境名称",
                value=environment.name if environment else "",
            ).classes("w-full")
            host = ui.input(
                "主机 IP",
                value=environment.host if environment else "",
            ).classes("w-full")
            port = ui.number(
                "端口号",
                value=environment.port if environment else 3306,
                min=1,
                max=65535,
            ).classes("w-full")
            user = ui.input(
                "用户名",
                value=environment.user if environment else "",
            ).classes("w-full")
            password = ui.input(
                "密码",
                value=environment.password if environment else "",
                password=True,
                password_toggle_button=True,
            ).classes("w-full")
            database = ui.input(
                "数据库名称",
                value=environment.database if environment else "",
            ).classes("w-full")

            def form_data() -> dict:
                return {
                    "id": environment.id if environment else None,
                    "env_type": env_type.value,
                    "name": name.value,
                    "host": host.value,
                    "port": int(port.value),
                    "user": user.value,
                    "password": password.value or "",
                    "database": database.value,
                }

            def test_connection() -> None:
                try:
                    service.test_environment_data(form_data())
                except Exception as error:
                    notify_error(error)
                    return
                notify_success("连接测试成功")

            def save() -> None:
                try:
                    _, synced_count = service.save_environment(form_data())
                except Exception as error:
                    notify_error(error)
                    return
                notify_success(f"保存成功，已同步 {synced_count} 条 Prompt 状态")
                dialog.close()
                environment_table.refresh()

            with ui.row().classes("justify-end w-full"):
                ui.button("取消", on_click=dialog.close).props("flat")
                ui.button("测试连接", on_click=test_connection).props("outline")
                ui.button("保存并同步", on_click=save)

        dialog.open()

    def edit_environment(environment_id: str) -> None:
        try:
            open_editor(service.get_environment(environment_id))
        except Exception as error:
            notify_error(error)

    def delete_environment(environment_id: str) -> None:
        try:
            environment = service.get_environment(environment_id)
        except Exception as error:
            notify_error(error)
            return

        with ui.dialog() as dialog, ui.card():
            ui.label(f"确认删除配置：{environment.display_name}")
            ui.label("本地状态记录会直接硬删除，不会影响远程 MySQL 数据。").classes(
                "text-sm text-gray-600"
            )

            def confirm() -> None:
                try:
                    service.delete_environment(environment.id)
                except Exception as error:
                    notify_error(error)
                    return
                notify_success("数据库环境配置已删除")
                dialog.close()
                environment_table.refresh()

            with ui.row().classes("justify-end w-full"):
                ui.button("取消", on_click=dialog.close).props("flat")
                ui.button("删除", on_click=confirm).props("color=negative")
        dialog.open()

    def sync_environment(environment_id: str) -> None:
        try:
            synced_count = service.test_and_sync(environment_id)
        except Exception as error:
            notify_error(error)
            return
        notify_success(f"连接成功，已同步 {synced_count} 条 Prompt 状态")

    def handle_action(event) -> None:
        action = event.args.get("action")
        environment_id = str(event.args["id"])
        if action == "edit":
            edit_environment(environment_id)
        elif action == "sync":
            sync_environment(environment_id)
        elif action == "delete":
            delete_environment(environment_id)

    ui.label("数据库环境配置").classes("text-xl font-semibold")
    ui.label(f"配置文件路径：{service.config_path}").classes("text-sm text-gray-600")
    with ui.row().classes("items-center gap-2"):
        ui.button("新增", on_click=lambda: open_editor())
    environment_table()
