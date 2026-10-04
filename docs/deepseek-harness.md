# DeepSeek Harness 原生插件

本包提供真正的 Cordis 插件入口和 bundle 配置：DeepSeek Harness 加载后，模型可调用六个研究工具。插件复用包内固定版本的 Kaggle 索引、方法卡和研究场景，工具查询不需要 DeepSeek、Kaggle 或 GitHub token。对话的模型与账户由 Harness 本身配置。

## 安装

需要 Python 3.10+；本项目的 Node.js 最低版本是 20，Harness 自身的运行要求还应以其对应版本为准。当前兼容验证使用官方 npm 发布的 `@deepseek-ai/dsh@0.2.0-rc.2` 工具契约。

从本项目 [Releases](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases) 下载最新的 `haoxuanjng-lang-kaggle-solutions-skills-<version>.tgz`，通过 Harness 官方的 profile 安装命令添加：

```bash
npx @deepseek-ai/dsh@0.2.0-rc.2 plugin --profile kaggle add ./haoxuanjng-lang-kaggle-solutions-skills-<version>.tgz
npx @deepseek-ai/dsh@0.2.0-rc.2 --profile kaggle --dump-config
npx @deepseek-ai/dsh@0.2.0-rc.2 --profile kaggle
```

将文件名中的 `<version>` 替换为下载的实际版本。`--dump-config` 应显示本包的 bundle 层和 `kaggle-solutions-research` 插件行。发布的 JavaScript 已可直接加载，没有安装时的 build script。

已有 Harness Web profile 的用户也可以在插件管理页面安装同一 tarball；安装器调用官方 `plugin_manager.install_bundle`，而不是将 `SKILL.md` 冒充插件模块。替换已安装包后需重启 Harness 以加载新的 JavaScript 模块。

## 工具与使用方式

| 工具 | 输入 | 输出 |
|---|---|---|
| `kaggle_solutions_stats` | 无 | 真实快照数量、来源版本、已读来源统计 |
| `kaggle_solutions_search` | `query`；可选 `modality`、`limit`、`topRank`、`solutionsLimit` | 同构比赛线索和档案链接 |
| `kaggle_solutions_show` | `competition`；可选排名和链接数量 | 某场比赛的档案记录 |
| `kaggle_solutions_patterns` | 可选 `query` | 有出处、迁移条件和最小对照实验的方法卡 |
| `kaggle_research_scenarios` | 无 | 真实历史比赛研究场景列表 |
| `kaggle_research_plan` | `scenario`、绝对路径 `outputDir` | 五个研究角色任务包与依赖图，写入指定 workspace |

例如向 Harness 提出：

> 使用 kaggle_solutions_show 查询 OTTO 推荐系统比赛，再用 kaggle_solutions_patterns 查 retrieval。保留档案链接、作者报告和迁移推断的区别。

> 列出 kaggle_research_scenarios，为 otto 创建研究任务包。并行分配来源阅读、验证审查和迁移分析，完成后由合成角色汇总。不要把生成任务包当作 agent 已执行。

研究计划工具只生成角色任务和结果契约。实际调度使用当前 Harness 配置中已有的 subagent/workflow 工具；本包不会自行启动付费模型调用，也不包含第二套比赛训练或提交工作流。

## 本机配置

插件 `config` 接受以下字段，在激活时验证配置；未提供字段使用默认值。

| 字段 | 默认值 | 用途 |
|---|---|---|
| `python` | `python` | Python 可执行文件名或绝对路径；路径带空格无需额外 shell 引号 |
| `timeoutMs` | `30000` | 单次查询或计划生成的超时，最大 300000 |
| `maxBufferBytes` | `8388608` | 子进程输出字节上限，最大 67108864 |
| `workspaceRoot` | Harness 启动时的工作目录 | 计划输出必须位于该绝对路径下 |

需要输出计划时，指定已经存在的工作目录，在 profile 的用户 patch 中覆盖完整配置，例如：

```yaml
- id: kaggle-solutions-research
  config:
    python: python
    timeoutMs: 30000
    maxBufferBytes: 8388608
    workspaceRoot: 'D:/Kaggle/research-workspaces'
```

`outputDir` 必须是 workspace 中尚未存在的新子目录，其父目录必须已存在。插件解析父目录的真实路径以检查符号链接/junction，禁止覆盖安装包、源代码或 workspace 本身。读取工具不写入 workspace；所有 Python 调用使用参数数组和 `shell: false`，观察调用方取消信号。

## 兼容性验证与限制

开发者可复现本次官方运行时测试：

```bash
npm install --prefix cache/deepseek-runtime --ignore-scripts --no-audit --no-fund --package-lock=false @deepseek-ai/dsh-tools@0.2.0-rc.2 @deepseek-ai/cordis@4.0.4
```

PowerShell：

```powershell
$env:DEEPSEEK_RUNTIME_NODE_MODULES = (Resolve-Path cache/deepseek-runtime/node_modules).Path
node --test tests/deepseek-plugin.test.mjs
```

macOS / Linux：

```bash
DEEPSEEK_RUNTIME_NODE_MODULES="$PWD/cache/deepseek-runtime/node_modules" node --test tests/deepseek-plugin.test.mjs
```

测试覆盖实际官方 Cordis `Context`、官方 `SystemPrompt` 和 `ToolRuntime` 的加载、六个工具注册、Python 查询执行、规范 JSON 结果、错误传播及卸载清理，并验证工作目录限制、五角色任务生成和未派发状态。未设置该环境变量时，普通离线测试仍会执行，官方运行时测试明确显示 skipped。

此外，已在维护者本机安装的 `@deepseek-ai/dsh@0.1.0-rc.6` 中安装本地发行构建、启动完整 Web host，并通过真实 host pipeline 成功调用全部六个工具。插件管理页面显示已挂载、已启用；旧版界面显示模块名称，未显示导出的双语标题和自定义图标。完整证据与凭据兼容处理见 [本机验证记录](harness-local-validation.md)。未进行带 API Key 的模型对话或 Kaggle 计分运行。

官方 Harness 目前处于 developer preview，后续版本可能更改接口。本次参考固定在源码提交 [`5badb15009ae1756c3afe0ae0cef1faafc290ccc`](https://github.com/deepseek-ai/deepseek-harness/tree/5badb15009ae1756c3afe0ae0cef1faafc290ccc)，并以已发布的 `0.2.0-rc.2` npm 运行时完成上述测试；没有声称当前 master 的完整应用已经重建或全部未来版本兼容。

官方依据：[插件打包与 profile 安装](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/docs/user/develop/basic/publish.md)、[工具注册与执行契约](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/docs/cookbook/adding-a-tool.md)、[Host bundle 与显示元数据](https://github.com/deepseek-ai/deepseek-harness/blob/5badb15009ae1756c3afe0ae0cef1faafc290ccc/packages/preset/agent-preset/skills/cordis-plugin-development/references/host-plugin.md)。本集成由本项目维护，并非 DeepSeek 官方发布的 Kaggle 插件。
