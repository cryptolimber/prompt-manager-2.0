"""程序入口。"""

from __future__ import annotations

import logging
import sys

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


def configure_console_logging() -> None:
    """让源码运行和 exe 运行时的日志都输出到当前终端。"""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
        force=True,
    )
    for logger_name in ("nicegui", "uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(logger_name).setLevel(logging.INFO)


def run_app() -> None:
    LocalStatusRepository().initialize()
    print("Prompt Manager 2.0 正在启动...", flush=True)
    print("访问地址：http://localhost:8080", flush=True)
    print("保持该终端窗口打开，关闭窗口会停止服务。", flush=True)
    ui.run(
        title="Prompt Manager 2.0",
        reload=False,
        uvicorn_logging_level="info",
    )


def wait_before_exit_when_packaged() -> None:
    if not getattr(sys, "frozen", False):
        return
    print("", flush=True)
    print("程序异常退出，按回车键关闭窗口...", flush=True)
    try:
        input()
    except EOFError:
        pass


def main() -> None:
    configure_console_logging()
    try:
        run_app()
    except Exception:
        logging.exception("Prompt Manager 2.0 启动失败")
        wait_before_exit_when_packaged()
        raise


if __name__ in {"__main__", "__mp_main__"}:
    main()
