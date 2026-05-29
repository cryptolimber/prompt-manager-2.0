# 项目需求档案

本文件用于记录项目需求的分析、拆分、完成点和后续事项，避免后续工作失忆。

## 使用规则

- 每次处理需求前，先阅读本文件。
- 开始实现前，先记录或确认需求目标、范围、约束和验收点。
- 需求较复杂时，拆分为可执行任务。
- 完成需求后，记录完成点、验证结果和后续事项。
- 历史记录以追加为主；如需修正，应保留事实脉络。

## 需求记录模板

### YYYY-MM-DD：需求标题

- 需求内容：
- 需求分析：
- 任务拆分：
- 完成点：
- 验证结果：
- 后续事项：

## 需求记录

### 2026-05-21：使用 `uv` 管理 Python 3.12 环境

- 需求内容：使用 `uv` 管理当前项目的虚拟环境，Python 版本使用 3.12。
- 需求分析：项目需要明确 Python 版本和环境管理方式；当前项目暂无源码和依赖，因此先建立基础项目配置、版本约束和忽略规则。
- 任务拆分：新增 `pyproject.toml`；新增 `.python-version`；新增 `.gitignore`；更新 `AGENTS.md` 中的项目环境规则；运行 `uv sync` 验证环境配置。
- 完成点：已配置 `requires-python = ">=3.12,<3.13"`；已配置 `.python-version` 为 `3.12`；已配置 `.venv` 等本地缓存忽略规则；已记录 `uv` 使用约定。
- 验证结果：已运行 `uv sync` 创建 `.venv` 并生成 `uv.lock`；已通过 `uv run python --version` 确认当前环境为 Python 3.12.3。
- 后续事项：项目新增依赖时，通过 `uv add` 或更新 `pyproject.toml` 后再运行 `uv sync`。

### 2026-05-21：添加项目记忆和需求档案

- 需求内容：为项目添加 Codex 官方项目记忆文件，并新增专门记录需求处理过程的 `PROJECT.md`。
- 需求分析：项目需要长期保留协作原则、需求处理规则和需求完成记录，避免后续工作缺少上下文。
- 任务拆分：创建并更新 `AGENTS.md`；创建 `PROJECT.md`；把需求处理原则和 `PROJECT.md` 使用方法写入项目记忆。
- 完成点：已添加 `AGENTS.md`；已添加 `PROJECT.md`；已记录中文描述规则、需求处理原则和需求档案使用方法。
- 验证结果：已通过文件内容检查确认记录存在。
- 后续事项：后续每次完成需求后，需要继续更新本文件。

### 2026-05-21：参考《项目概览.md》搭建 Prompt 管理工具首版

- 需求内容：基于《项目概览.md》搭建 Prompt Manager 2.0 项目，形成可运行的 NiceGUI 桌面端/网页端工具首版。
- 需求分析：项目需要管理三个固定 MySQL 环境，支持本地配置持久化、Prompt 分页查看、详情、编辑、删除状态维护、本地 SQLite 同步状态表，以及开发环境向测试/预发布环境按选中数据条目推送；代码需要按配置、数据库、仓储、服务、界面和工具模块拆分。
- 任务拆分：补充 NiceGUI、Peewee、PyMySQL 依赖；创建 `prompt_manager_2_0` 包结构；实现配置文件读写；实现 MySQL/SQLite 连接和 Peewee 模型；实现 Prompt 仓储、本地状态仓储、环境服务、同步服务、编辑服务和发布服务；实现数据库环境配置页、Prompt 管理页和程序入口。
- 完成点：已实现用户目录 `PROMPT_MANAGER_CONFIG.json` 配置读写；已实现用户目录 `.prompt_manager_2_0/local_status.db` 本地 SQLite 状态库；已实现环境新增/编辑时连接测试和同步；已实现环境删除时本地状态软删除；已实现 Prompt 分页查询、详情、编辑和删除；已实现从开发环境向测试/预发布环境推送选中 Prompt；已更新 `pyproject.toml` 和 `uv.lock`。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv sync` 完成依赖同步；已运行 `.venv/bin/python -m compileall prompt_manager_2_0` 和 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0` 通过语法检查；已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from prompt_manager_2_0.main import index; print('import ok')"` 通过入口导入检查；已启动 NiceGUI，输出地址为 `http://localhost:8080`，但当前沙箱网络无法通过 `curl` 访问该监听地址，待在用户本机浏览器确认界面。
- 后续事项：需要使用真实 MySQL 环境验证远程连接、表结构兼容性、分页查询、编辑写回和推送策略；如需严格桌面窗口模式，后续可评估 NiceGUI native/pywebview 打包方案。

### 2026-05-21：调整数据库环境页面操作入口

- 需求内容：将数据库环境页面的编辑、同步、删除按钮移动到表格每条记录最右侧，并将测试连接按钮放到新增配置弹窗中。
- 需求分析：当前页面需要先选中表格行再点击顶部按钮，操作路径较间接；把行级操作放在每条记录末尾更符合管理表格的使用习惯。测试连接属于配置表单校验能力，放入新增/编辑弹窗中更便于保存前验证。
- 任务拆分：环境表格增加操作列；移除顶部编辑、测试并同步、删除按钮；新增行级编辑、同步、删除图标按钮；服务层增加未保存表单数据的连接测试方法；弹窗增加测试连接按钮。
- 完成点：数据库环境表格最右侧已提供编辑、同步、删除行级按钮；顶部仅保留新增按钮；新增/编辑弹窗底部已提供测试连接按钮；保存仍保留保存并同步逻辑。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0` 通过语法检查；已运行环境页面和服务层导入检查；已重启 NiceGUI，输出地址为 `http://localhost:8080`。
- 后续事项：需要在浏览器中确认表格 action 列布局和弹窗按钮位置符合预期，并使用真实 MySQL 配置验证测试连接、同步、删除流程。

### 2026-05-21：优化本地 SQLite 与 Navicat 并发访问

- 需求内容：解决 Navicat 和服务同时使用本地 SQLite 状态库时容易出现 `database is locked` 的问题。
- 需求分析：原实现初始化 SQLite 时会打开连接并长期持有，Navicat 同时连接同一数据库文件时容易产生锁冲突；SQLite 仍然只能串行写入，但可以通过 WAL、短连接和等待超时降低读写冲突。
- 任务拆分：SQLite 连接增加 `timeout=10` 和 `busy_timeout=10000`；初始化方法只负责创建目录，不再长期持有连接；本地状态仓储所有操作改成 `connection_context()` 临时连接，用完自动关闭；补回包内 `prompt_manager_2_0/main.py`，保证 `python -m prompt_manager_2_0` 可用。
- 完成点：本地 SQLite 连接已改成操作级短连接；初始化建表、同步写入、软删除、硬删除和修改标记都已用临时连接包裹；服务空闲时不会继续占用 SQLite 连接。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已用临时 HOME 执行本地 SQLite 初始化检查；已确认初始化后 `sqlite_database.is_closed()` 为 `True`；8080 端口已有服务占用，因此已在 `http://localhost:8081` 启动新实例验证新代码可运行。
- 后续事项：Navicat 和服务仍不应同时长时间写入同一 SQLite 文件；如需人工查看，优先在 Navicat 使用只读连接或避免在服务同步时修改同表数据。

### 2026-05-21：排查 Navicat 仍提示 SQLite locked

- 需求内容：关闭旧 8080 服务后，Navicat 打开本地 SQLite 仍提示 `database is locked`，需要确认原因并处理。
- 需求分析：8080 旧服务已关闭，但 8081 新服务仍在运行；排查发现当前没有进程长期占用 `local_status.db`、`local_status.db-wal`、`local_status.db-shm`，Python 可正常打开数据库并通过 `PRAGMA quick_check`，说明主库未损坏且不是服务长期持锁。目录中残留 WAL/SHM 文件可能导致 Navicat 旧连接继续感知锁状态。
- 任务拆分：检查数据库文件占用；检查 8080/8081 服务进程；执行 SQLite `PRAGMA quick_check`；执行 `PRAGMA wal_checkpoint(TRUNCATE)` 合并并截断 WAL。
- 完成点：已确认 8080 无占用；8081 是当前新服务；已执行 WAL checkpoint，返回 `(0, 0, 0)`；目录中已只剩 `local_status.db`，`local_status.db-wal` 和 `local_status.db-shm` 已消失。
- 验证结果：`PRAGMA journal_mode` 为 `wal`；`PRAGMA quick_check` 返回 `ok`；WAL checkpoint 成功。
- 后续事项：Navicat 若仍报锁，需要关闭 Navicat 当前 SQLite 连接或所有表编辑窗口后重新打开主库文件；避免在服务执行同步写入时由 Navicat 同时编辑同一张表。

### 2026-05-21：调整 Prompt 推送目标环境选择流程

- 需求内容：将 Prompt 管理页的“推送选中”按钮移动到页面右端，与表格右侧对齐，并与“查询”按钮处于同一水平；未选中数据条目时提示用户；已选中数据条目时弹出目标环境选择窗口，窗口包含取消和推送按钮。
- 需求分析：原页面把目标环境选择框常驻在查询区下方，推送流程占用页面空间且缺少明确确认步骤；改为先选数据条目，再通过弹窗选择目标环境，可降低误操作并让主页面布局更紧凑。
- 任务拆分：移除页面常驻目标环境下拉框；查询工具行右侧增加“推送选中”按钮；点击推送时先校验选中数据条目；弹窗内加载测试环境和预发布环境作为目标环境；弹窗提供取消和推送操作。
- 完成点：“推送选中”已移动到查询行最右侧；未选择数据条目时提示“请先选择需要推送的数据条目”；选择数据条目后弹出“推送目标环境”窗口；推送确认后调用原发布服务。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行 Prompt 管理页面导入检查；已重启 8080 端口服务。
- 后续事项：需要在浏览器中确认按钮右对齐效果、弹窗流程和真实环境推送结果。

### 2026-05-21：固定管理表格高度并启用内部滚动

- 需求内容：Prompt 管理页面和数据库环境配置页面的表格都需要固定高度；当表格行数超过高度时，在表格块内部显示滚动条，避免外部 UI 被内容撑开导致样式抖动。
- 需求分析：表格内容高度随数据量变化会影响页面整体布局稳定性；通过固定表格容器高度并启用 `overflow-auto`，可以把滚动限制在表格区域内。
- 任务拆分：数据库环境配置表格外层增加固定高度滚动容器；Prompt 管理表格外层增加固定高度滚动容器；给表格设置最小宽度以保证横向空间不足时也在容器内滚动。
- 完成点：数据库环境配置表格容器高度固定为 `520px`；Prompt 管理表格容器高度固定为 `560px`；两个表格均启用内部滚动，不再由行数撑开外层页面。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已重启 8080 端口服务。
- 后续事项：需要在浏览器中确认不同数据量下滚动条位置、分页栏显示和移动端宽度表现。

### 2026-05-21：调整 Prompt 表格分页控件布局

- 需求内容：Prompt 表格每页展示条数由“每页数量”下拉框控制；隐藏表格内置的 `records per page` UI；将“每页数量”下拉框放到 Prompt 表格左下角并与表格左侧对齐。
- 需求分析：项目已使用自定义分页逻辑查询远程 MySQL 当前页数据，表格内置分页 UI 会造成重复控制和误解；把每页数量放到表格底部，与总数和翻页控件形成统一分页区。
- 任务拆分：移除顶部查询行中的每页数量下拉框；给 Prompt 表格增加 `hide-pagination` 属性；在表格底部左侧新增每页数量下拉框；右侧保留总数、页码、上一页和下一页。
- 完成点：Prompt 表格内置 `records per page` UI 已隐藏；每页数量下拉框已移动到表格左下角；下拉框仍控制服务端分页条数。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行 Prompt 管理页面导入检查；已重启 8080 端口服务。
- 后续事项：需要在浏览器中确认 NiceGUI/Quasar 的 `hide-pagination` 在当前版本下完全隐藏内置分页栏。

### 2026-05-21：修复 Prompt 每页数量切换后表格行数不联动

- 需求内容：修复 Prompt 管理页中“每页数量”切换后，右下角页数已更新但表格实际展示行数不联动的问题。
- 需求分析：表格虽然隐藏了内置分页 UI，但内部仍按 `pagination=state["page_size"]` 管理行数；外部下拉框改变服务端分页条数后，表格内部分页状态可能继续截断当前 rows，导致显示行数不符合外部选择。
- 任务拆分：移除刷新时对 `table.pagination` 的动态赋值；将 NiceGUI 表格内部分页固定为 `{"rowsPerPage": 0}`，表示展示当前后端返回的全部 rows；保留外部每页数量下拉框控制后端查询条数。
- 完成点：Prompt 表格内部分页不再截断后端返回的数据；每页数量切换后，表格 rows 和页数使用同一份 `state["page_size"]` 查询结果。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行 Prompt 管理页面导入检查；已重启 8080 端口服务。
- 后续事项：需要用真实数据分别选择 10、15、20 验证表格行数和页数同时变化。

### 2026-05-21：隐藏数据库环境表格原生分页

- 需求内容：隐藏数据库环境配置页面表格右下角的原生页数和每页展示条数，数据库环境配置数据直接全部展示。
- 需求分析：数据库环境配置数量有限，不需要分页；保留原生分页会增加无效控件，也和固定高度滚动容器的交互重复。
- 任务拆分：将数据库环境配置表格内部分页设置为 `{"rowsPerPage": 0}`；增加 `hide-pagination` 属性隐藏原生分页栏。
- 完成点：数据库环境配置表格已直接展示全部配置项；表格右下角原生页数和每页展示条数已隐藏；超过固定高度时由外层容器滚动。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行数据库环境页面导入检查；已重启 8080 端口服务。
- 后续事项：需要在浏览器中确认环境配置较多时内部滚动正常。

### 2026-05-21：调整 Prompt 表格对齐、序号和描述展示

- 需求内容：Prompt 管理表格中表头字段和每条记录的值都左对齐；在选中框后、`id` 前增加序号列，标注当前数据是第多少条；`description` 只显示 15 个字，剩余内容用 `...` 隐藏。
- 需求分析：表格需要提升可读性和定位效率；序号应按当前分页位置计算为全局序号；描述截断只影响列表展示，不应影响详情和编辑中的完整内容。
- 任务拆分：Prompt 表格列增加 `align="left"`；新增 `序号` 列并放在字段列最前；加载行数据时按 `(当前页 - 1) * 每页数量 + 行索引` 计算序号；新增列表描述截断逻辑。
- 完成点：Prompt 表头和单元格已左对齐；选中框后已显示序号列；`description` 超过 15 个字符时按 `前 15 个字符 + ...` 展示；详情和编辑仍从远程数据库读取完整记录。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已验证描述截断函数输出；已重启 8080 端口服务。
- 后续事项：需要在浏览器中确认序号列位置、左对齐效果和中文/英文混合描述截断显示。

### 2026-05-21：固定 Prompt 表格序号列和操作列

- 需求内容：Prompt 表格的序号字段固定到最左端，操作字段固定到最右端，表格当前宽度固定。
- 需求分析：Prompt 表格字段较多，横向滚动时需要保留行定位信息和操作入口；选择框列与序号列需要一起固定在左侧，操作列固定在右侧，表格容器保持页面当前宽度，横向溢出只在表格内部滚动。
- 任务拆分：为 Prompt 表格增加专用 CSS；固定选择框列、序号列和操作列；设置表格容器 `100%` 宽度和内部滚动；设置表格最小宽度，避免字段挤压导致布局变形。
- 完成点：Prompt 表格选择框列和序号列已固定在左侧；操作列已固定在右侧；表格容器宽度固定为页面当前宽度，横向内容通过内部滚动查看。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行 Prompt 表格样式导入检查；已重启 8080 端口服务。
- 后续事项：需要在浏览器中横向滚动确认固定列层级、阴影边界和 hover 背景显示。

### 2026-05-21：收紧 Prompt 管理页布局并调整操作列图标

- 需求内容：跳转到 Prompt 管理界面时不应触发页面级滚动条，需要适当收紧布局；Prompt 表格操作列的三个图标需要在同一水平，并适当占用左侧空间。
- 需求分析：原 Prompt 表格固定高度为 `560px`，叠加标题、工具栏和底部分页控件后容易触发页面级滚动；操作列固定宽度偏紧时，三个图标存在换行或拥挤风险。
- 任务拆分：将 Prompt 表格容器高度改为基于视口的响应式高度，最大 `500px`、最小 `340px`；Prompt 表格启用 dense 模式；操作列宽度从 `132px` 调整为 `148px`；操作按钮行改为不换行的专用布局。
- 完成点：Prompt 管理页布局已收紧；表格容器高度会随视口收缩，避免页面外层滚动；操作列三个图标已设置为同一水平不换行展示。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行 Prompt 页面导入检查；已重启 8080 端口服务。
- 后续事项：需要在浏览器中确认当前分辨率下页面不出现外层滚动条，操作列按钮不换行。

### 2026-05-21：调整 Prompt 编辑框高度和拖拽行为

- 需求内容：Prompt 记录编辑界面中，`prompt_content` 编辑框当前高度需要为最小高度，支持向下拖动增加高度，并让下面的编辑字段依次向下排列。
- 需求分析：`prompt_content` 内容较长，需要允许用户按需扩大输入区域；编辑框拖动时不能覆盖后续字段，弹窗也需要在内容较高时支持内部滚动。
- 任务拆分：为 Prompt 编辑弹窗增加内部滚动样式；为 `prompt_content` 文本框设置初始行数和最小高度；通过 CSS 允许文本框纵向 resize。
- 完成点：`prompt_content` 编辑框初始为 4 行、最小高度为 `96px`；文本框支持向下拖动增加高度；后续字段保持正常文档流向下排列；弹窗高度超过视口时在弹窗内部滚动。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行 Prompt 页面导入检查；已重启 8080 端口服务。
- 后续事项：需要在浏览器中确认不同浏览器对 textarea 右下角拖拽手柄的显示一致性。

### 2026-05-22：Prompt 详情弹窗支持复制 code

- 需求内容：在 Prompt 管理界面中，每条数据的详情弹窗里，在 `code` 码右侧添加复制按钮，点击后把对应 `code` 复制到剪贴板。
- 需求分析：`code` 是 Prompt 的关键标识，详情查看时常需要复制；复制按钮只应出现在详情弹窗的 `code` 字段行，不影响其他字段展示。
- 任务拆分：确认 NiceGUI 剪贴板 API；修改详情弹窗字段渲染；在 `code` 行右侧增加复制按钮；点击后调用 `ui.clipboard.write` 并提示复制成功。
- 完成点：Prompt 详情弹窗的 `code` 行右侧已新增“复制”按钮；点击按钮会复制当前记录的 `code` 值并显示“code 已复制”提示。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行 Prompt 页面导入检查；已启动 8080 端口服务。
- 后续事项：需要在浏览器中确认剪贴板权限提示和复制结果；部分浏览器要求页面处于安全上下文或用户点击事件中执行剪贴板写入。

### 2026-05-22：Prompt 编辑页禁用租户、机构和创建时间字段

- 需求内容：Prompt 记录编辑界面中，`tenant_id`、`org_id`、`create_time` 不能修改，需要设为 disable 状态。
- 需求分析：这三个字段属于来源上下文和创建元数据，不应在 Prompt 内容维护时被修改；仅在界面禁用仍可能被提交，因此保存逻辑也需要排除这三个字段。
- 任务拆分：将 `tenant_id`、`org_id`、`create_time` 从可编辑字段常量中移出；新增只读编辑字段常量；编辑弹窗中展示这三个字段并设置 `disable`；保存时只提交真正可编辑字段。
- 完成点：编辑界面中 `tenant_id`、`org_id`、`create_time` 已禁用展示；保存请求不会提交这三个字段；远程更新逻辑不再处理这三个字段。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已确认可编辑字段列表不包含 `tenant_id`、`org_id`、`create_time`；已重启 8080 端口服务。
- 后续事项：需要在浏览器中确认禁用态样式清晰，保存编辑时这三个字段不发生变化。

### 2026-05-22：Prompt 管理面板新增 PROMPT 表单

- 需求内容：在 Prompt 管理面板添加新增 PROMPT 的表单逻辑和按钮，按钮需要与查询按钮水平对齐。
- 需求分析：新增 Prompt 需要写入当前选中的远程 MySQL 环境，并同步一条本地 SQLite 状态记录；新增时需要录入完整记录字段，创建后 `tenant_id`、`org_id`、`create_time` 仍按编辑规则不可修改。
- 任务拆分：仓储层新增 `create_prompt`；服务层新增 `create_prompt` 并写入本地状态表；Prompt 管理工具栏在查询按钮右侧增加“新增 PROMPT”按钮；新增弹窗包含 `aiag_prompt_template` 全字段表单，`create_time` 默认当前时间，`is_active` 和 `status` 默认 `1`。
- 完成点：点击“新增 PROMPT”会打开新增表单；保存后向当前环境远程 MySQL 插入记录；新增成功后刷新第一页列表；本地状态表同步新增记录状态。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行新增仓储和 Prompt 页面导入检查；已重启 8080 端口服务。
- 后续事项：需要使用真实 MySQL 验证新增字段约束、主键冲突提示和本地状态同步结果。

### 2026-05-22：调整新增和编辑 Prompt 字段规则

- 需求内容：新增 Prompt 表单中 `id` 字段由数据库自动生成；`create_time` 由代码自动生成并回填表单；编辑 Prompt 表单允许修改 `tenant_id` 和 `org_id`。
- 需求分析：新增记录时主键应依赖远程 MySQL 自增能力，避免人工输入主键；创建时间由应用生成后展示给用户但不需要手动填写；租户和机构字段在编辑场景需要允许维护。
- 任务拆分：新增表单移除 `id` 字段；新增表单 `create_time` 默认当前时间并禁用展示；仓储新增逻辑不再要求 `id`，插入后读取数据库生成的主键；可编辑字段恢复 `tenant_id` 和 `org_id`，只读字段仅保留 `create_time`。
- 完成点：新增 Prompt 时不再提交 `id`；新增后使用数据库生成的主键同步本地状态；新增表单 `create_time` 由代码生成并回填；编辑表单中 `tenant_id` 和 `org_id` 已恢复可编辑。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已确认可编辑字段包含 `tenant_id` 和 `org_id`，只读字段仅包含 `create_time`；已重启 8080 端口服务。
- 后续事项：需要用真实 MySQL 验证 `id` 自增字段是否与 Peewee 模型兼容，以及新增后本地 SQLite 状态表是否记录正确主键。

### 2026-05-22：Prompt 软删除过滤和 code 唯一校验

- 需求内容：Prompt 记录中 `status=0` 表示软删除，不显示在列表中；在 `status` 非 0 的 Prompt 中，`code` 字段需要唯一。
- 需求分析：列表应只展示非软删除数据；`code` 是业务唯一标识，但软删除记录可保留历史 code，不参与活跃数据唯一性判断。该规则需要在仓储层统一实现，避免新增、编辑和推送写入绕过校验。
- 任务拆分：列表总数和分页查询增加非软删除条件；新增 Prompt 时校验非软删除记录中的 `code` 唯一；编辑 Prompt 时按更新后的 `code/status` 校验唯一；推送写入目标环境时同样校验非软删除 `code` 唯一。
- 完成点：`status=0` 的 Prompt 不再出现在 Prompt 管理列表；新增、编辑和发布 upsert 时，如果目标环境中存在相同 `code` 且非软删除的其他记录，会提示“非软删除 Prompt 中 code 必须唯一”。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行 Prompt 仓储导入检查；已重启 8080 端口服务。
- 后续事项：需要使用真实 MySQL 验证已有重复活跃 `code` 数据的提示行为，以及 `status=0` 记录是否从分页总数和列表中排除。

### 2026-05-22：数据库配置去重、本地状态硬删除和环境权限收敛

- 需求内容：同一 `IP:端口:数据库` 只能添加一条数据库配置；删除数据库配置时本地 SQLite 状态记录改为硬删除；删除 Prompt 时远程仍只做 `status=0` 软删除，本地状态记录硬删除；Prompt 详情新增本地最近更新时间；只有开发环境允许新增、编辑、删除和推送 Prompt，测试/预发布环境只能查看详情，推送方向限制为开发环境到测试或预发布环境。
- 需求分析：本工具只操作 `aiag_prompt_template` 表，因此环境类型不同但数据库地址相同仍属于重复配置；本地状态表用于当前软件的同步状态，不再保留已删除配置或已删除 Prompt 的软删除记录；最近更新时间来自本地 SQLite 的 `last_modify_time`；权限限制需要同时在 UI 和服务层实现，避免绕过页面直接调用写操作。
- 任务拆分：调整数据库唯一标识为 `host:port:database`；保存环境前按该标识去重；删除环境时硬删除新旧标识下的本地状态记录；Prompt 编辑/新增/推送后更新本地状态时间，详情读取并展示最近更新时间；Prompt 新增、编辑、删除服务层校验开发环境；页面在非开发环境隐藏新增和推送入口并禁用编辑/删除按钮；推送服务校验开发到测试/预发布且源目标不能指向同一数据库。
- 完成点：数据库配置保存会阻止重复 `IP:端口:数据库`；环境删除和 Prompt 删除会硬删除本地 SQLite 状态记录；远程 Prompt 删除仍通过 `status=0` 软删除；详情弹窗已新增“最近更新时间”；测试和预发布环境在页面中只能查看详情，服务层也会拒绝新增、编辑、删除；推送仍按选中的 Prompt ID upsert 到目标环境，不做全库覆盖。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行 Prompt 页面、环境服务、Prompt 服务和推送服务导入检查；已用临时配置验证重复数据库配置校验会阻止新增重复项且允许编辑自身。
- 后续事项：需要使用真实 MySQL 分别验证开发到测试、开发到预发布的推送结果，以及测试/预发布环境页面的禁用态是否符合实际操作预期。

### 2026-05-22：Prompt 表格展示最近更新时间并改为 ID 升序

- 需求内容：最近更新时间除详情弹窗外，还需要展示在 Prompt 表格 `is_active` 后面；没有最近更新时间时显示“无更新”；从数据库查询 Prompt 数据时按 `id` 升序查询。
- 需求分析：最近更新时间来自本地 SQLite 状态表，应在列表查询后批量补充，避免表格逐行查询；升序排序需要在远程 Prompt 仓储层统一调整，保证列表和同步读取顺序一致。
- 任务拆分：本地状态仓储增加按 Prompt ID 批量读取最近更新时间；Prompt 列表服务把本地最近更新时间合并到每行数据；表格列在 `is_active` 后新增“最近更新时间”；无本地状态时展示“无更新”；远程分页查询和全量查询改为 `id asc`。
- 完成点：Prompt 表格已在 `is_active` 后显示“最近更新时间”；详情弹窗和表格无更新时间时均显示“无更新”；远程 Prompt 分页列表和全量同步查询都按 `id` 升序读取。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行组件格式化检查，确认无最近更新时间时返回“无更新”。
- 后续事项：需要在浏览器中用真实数据确认最近更新时间列的位置和 ID 升序展示符合预期。

### 2026-05-22：初始化 Git 仓库并提交初版

- 需求内容：为当前项目添加 `.git` 管理，并将初次提交信息设置为 `prompt_manager_2.0 v1 初版`。
- 需求分析：当前项目目录尚未初始化 Git 仓库；提交前需要确认 `.gitignore` 不会把 `.venv`、缓存和 IDE 本地文件纳入版本管理。
- 任务拆分：初始化 Git 仓库；补充忽略 `.idea/`；检查待提交文件；执行初次提交。
- 完成点：已初始化 Git 仓库；`.gitignore` 已忽略 `.idea/`、`.venv/` 和 Python 缓存；项目源码、配置、锁文件、需求档案和项目概览已纳入初次提交。
- 验证结果：已执行 `git status --ignored --short` 确认 `.idea/`、`.venv/` 和缓存目录处于忽略状态；已创建提交 `prompt_manager_2.0 v1 初版`。
- 后续事项：如后续需要推送远程仓库，需要再配置 remote 并执行 push。

### 2026-05-22：补充 PyInstaller 绿色包打包约定

- 需求内容：使用 PyInstaller 方式打包项目；在当前项目下新建 `dist/` 目录，每次打包产物都放入该目录；新增 `打包文档.md` 记录详细步骤；明确 Linux 环境能否直接打包 Windows 可执行文件。
- 需求分析：绿色包目标是不要求用户电脑预装 Python；PyInstaller 适合按平台生成可执行目录，但不能在 Linux 下直接可靠地产出 Windows `.exe`，Windows 包应在 Windows、Windows 虚拟机或 Windows CI 中构建。
- 任务拆分：补充构建依赖组；创建可被 Git 保留的 `dist/` 目录；忽略 `dist/` 中的实际打包产物和 `build/` 临时目录；新增打包文档，记录 Windows、macOS、Linux 的打包命令和验证清单。
- 完成点：已在 `pyproject.toml` 中新增 `build` 依赖组并加入 PyInstaller；已创建 `dist/.gitkeep` 保留打包目录；`.gitignore` 已忽略 `build/` 和 `dist/` 下的实际产物；已新增 `打包文档.md`，明确 Windows 包需要在 Windows 平台构建。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv lock` 更新 `uv.lock`，锁定 PyInstaller 及其相关依赖；已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run --group build pyinstaller --version` 确认 PyInstaller 版本为 `6.20.0`；已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查。
- 后续事项：需要分别在 Windows、macOS、Linux 目标平台执行文档中的打包命令，并在无 Python 环境机器上验证发行包运行效果。

### 2026-05-22：调整 exe 控制台驻留和日志输出

- 需求内容：exe 包启动后黑色控制台窗口需要驻留不消失，运行日志输出到该终端。
- 需求分析：Prompt Manager 2.0 是本地 Web 服务，控制台窗口应作为服务进程窗口保留；打包时不能使用 `--windowed` 或 `--noconsole`；程序启动日志、Uvicorn/NiceGUI 日志和异常堆栈需要直接输出到标准输出，便于用户反馈问题。
- 任务拆分：入口配置控制台日志；启动时输出访问地址和窗口关闭提示；打包环境下异常退出前等待用户按回车，避免窗口一闪而过；打包文档中的 PyInstaller 命令显式增加 `--console`。
- 完成点：入口已统一到包内 `prompt_manager_2_0.main`；启动时会在控制台输出服务地址和窗口关闭提示；日志已配置到标准输出；打包后的异常退出会等待用户按回车；打包文档已明确使用 `--console` 并提示不要使用 `--windowed` 或 `--noconsole`。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行入口导入检查；已重启 8080 服务，控制台输出启动提示、NiceGUI/Uvicorn 日志和访问日志。
- 后续事项：需要在 Windows 真实 exe 包中确认双击启动后控制台驻留、异常时暂停退出，以及用户关闭控制台会停止服务的行为符合预期。

### 2026-05-22：Windows 打包命令改为 CMD 格式

- 需求内容：`打包文档.md` 中 Windows 打包命令使用 CMD，而不是 PowerShell。
- 需求分析：PowerShell 使用反引号续行，CMD 使用 `^` 续行，两者不可混用；文档应直接给出 CMD 可复制执行的命令。
- 任务拆分：将 Windows 打包说明从 PowerShell 改为 CMD；代码块语言从 `powershell` 改为 `bat`；续行符从反引号改为 `^`。
- 完成点：`打包文档.md` 的 Windows 打包说明已改为 Windows CMD；PyInstaller 命令已使用 CMD 的 `^` 续行符。
- 验证结果：已检查文档片段，确认代码块为 `bat`，命令不再使用 PowerShell 反引号。
- 后续事项：需要在 Windows CMD 中实际执行一次打包命令，确认 uv 和 PyInstaller 在目标环境中可正常运行。

### 2026-05-29：Prompt 管理默认页和无分页列表

- 需求内容：打开系统后直接定位到 `PROMPT 管理`；Prompt 管理列表只保留一个滚动页面，按最新 Prompt 在前倒序展示，不再分页。
- 需求分析：用户主要操作入口是 Prompt 管理，默认落到数据库环境页会增加一步跳转；列表已有固定高度和内部滚动，取消分页后可直接通过滚动查看全部非软删除 Prompt。
- 任务拆分：调整首页 tab panel 默认值；Prompt 查询改为一次读取全部非软删除数据；远程查询按 `id` 倒序；移除 Prompt 页面每页数量、页码、上一页和下一页控件；清理不再使用的分页常量和仓储分页方法。
- 完成点：系统打开后默认选中 `Prompt 管理`；Prompt 管理表格展示全部查询结果；序号按当前倒序列表从 1 开始；底部仅显示总条数；列表继续通过表格固定高度区域滚动查看。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查。
- 后续事项：需要在浏览器中连接真实数据库确认最新数据是否按 `id` 倒序显示，且大数据量下表格内部滚动符合预期。

### 2026-05-29：调整 Prompt 管理刷新按钮文案

- 需求内容：将 Prompt 管理界面的 `查询` 按钮改名为 `刷新数据库`，并去掉按钮图标，避免误解为查询特定 Prompt。
- 需求分析：该按钮实际作用是重新读取当前选中数据库环境的 Prompt 列表，而不是按条件检索某条 Prompt；文案应表达刷新当前数据库数据的动作。
- 任务拆分：修改 Prompt 管理工具栏按钮文本；移除搜索图标；验证页面代码语法。
- 完成点：按钮已改为纯文本 `刷新数据库`，点击后仍调用当前数据库环境的列表刷新逻辑。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查。
- 后续事项：无。

### 2026-05-29：移除所有按钮图标

- 需求内容：将系统中所有按钮内部包含的图标全部去掉，只保留文字内容。
- 需求分析：当前数据库环境页、Prompt 管理页、弹窗底部操作和表格操作列仍存在图标按钮或图标加文字按钮；需要统一改成纯文字按钮，避免界面风格混杂。
- 任务拆分：移除所有 `ui.button` 的 `icon` 参数；将表格行操作中的纯图标按钮改为 `详情`、`编辑`、`删除`、`同步` 等文字按钮；适当调整 Prompt 操作列宽度；扫描源码确认不再存在 `icon` 配置。
- 完成点：数据库环境页、Prompt 管理页、详情/新增/编辑/删除/推送弹窗中的按钮均已改为纯文字；Prompt 表格操作列已加宽以容纳文字操作按钮。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行 `rg "icon" prompt_manager_2_0 -n` 确认应用源码无图标配置残留。
- 后续事项：需要在浏览器中确认文字按钮宽度和表格操作列显示效果。

### 2026-05-29：Prompt 管理新增字段模糊搜索

- 需求内容：在 Prompt 管理表格上方、按钮下方新增一行搜索控件；左侧下拉选择模糊搜索字段，支持 `code`、`description`、`version`、`category`；中间输入搜索内容；右侧为搜索按钮，三个组件同一水平，必须点击搜索按钮后才执行搜索。
- 需求分析：搜索应针对当前选中的数据库环境查询远程 `aiag_prompt_template` 表，并继续遵守非软删除过滤和 `id` 倒序展示；输入框变更不应自动触发查询，避免用户输入过程中频繁请求数据库。
- 任务拆分：新增 Prompt 搜索字段常量；仓储层增加可选字段模糊查询条件；服务层透传搜索条件并补充本地最近更新时间；Prompt 页面新增搜索行和搜索状态；点击 `搜索` 后更新搜索条件并刷新表格。
- 完成点：Prompt 管理页面已新增搜索字段下拉框、搜索内容输入框和 `搜索` 按钮；点击 `搜索` 才应用输入条件；`刷新数据库` 会清空搜索内容并重新加载当前数据库全量非软删除数据。
- 验证结果：已运行 `UV_CACHE_DIR=/tmp/uv-cache uv run python -m compileall prompt_manager_2_0 main.py` 通过语法检查；已运行 `rg "icon" prompt_manager_2_0 -n` 确认没有重新引入按钮图标配置。
- 后续事项：需要连接真实 MySQL 数据确认四个字段的模糊匹配结果和空搜索词返回全量数据的行为。
