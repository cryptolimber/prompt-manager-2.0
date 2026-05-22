"""程序入口。"""

from __future__ import annotations

from nicegui import ui

from prompt_manager_2_0.repositories.local_status_repository import (
    LocalStatusRepository,
)
from prompt_manager_2_0.ui.environment_page import create_environment_page
from prompt_manager_2_0.ui.prompt_manage_page import create_prompt_manage_page


@ui.page("/")
def index() -> None:
    ui.colors(primary="#2563eb")
    with ui.header().classes("items-center"):
        ui.label("Prompt Manager 2.0").classes("text-lg font-semibold")

    with ui.tabs().classes("w-full") as tabs:
        environment_tab = ui.tab("数据库环境")
        prompt_tab = ui.tab("Prompt 管理")

    with ui.tab_panels(tabs, value=environment_tab).classes("w-full"):
        with ui.tab_panel(environment_tab):
            create_environment_page()
        with ui.tab_panel(prompt_tab):
            create_prompt_manage_page()


def main() -> None:
    LocalStatusRepository().initialize()
    ui.run(title="Prompt Manager 2.0", reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
