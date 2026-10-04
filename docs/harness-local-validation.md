# 本机 Harness 验证记录

日期：2026-10-04（Asia/Shanghai）。本记录区分实际安装、真实 host 工具调用、UI 显示和模型对话。

## 验证环境与包

使用维护者本机已安装的全局 `@deepseek-ai/dsh@0.1.0-rc.6`，没有全局升级。Node.js 为 `24.15.0`，工具执行的 Python 为 `3.13.5`。专用 profile 名称是 `kaggle-solutions-validation`，独立 Web 端口为 `127.0.0.1:3082`，没有修改已有的 web 或 desktop profile。

通过真正的官方命令安装本地尚未发布的 tarball：

```text
dsh plugin --profile kaggle-solutions-validation add <local-dist>/haoxuanjng-lang-kaggle-solutions-skills-0.2.0.tgz
```

已验证的 tarball SHA256：

```text
f330f0a41d72fa233ef126294dca0a43d5fa699b0f784a057e58b160e4b0ef5f
```

这是当次验证构建的 hash；后续 README、文档或打包清单改变会产生不同 hash，发行资产应使用对应 Release 的校验文件。

## 安装、启动与实际工具结果

`dsh plugin` 安装退出码为 0。`--dump-config` 返回成功，包含本包 bundle 层及 `kaggle-solutions-research` 行。专用 profile 增加官方 `@deepseek-ai/dsh-web-app` 层后，完整 Web host 启动成功，首页 HTTP 200，启动 stderr 为空。

临时本地验证插件在真正启动的 host `Context` 中调用 `ctx.tools.schemas()` 和 `ctx.tools.execute()`，不是模拟 registry，也不是直接调用 Python 来代替 Harness 调用。返回了六个本包工具 schema，下列六次实际 host pipeline 调用均 `isError: false`：

| 调用 | 实际结果 |
|---|---|
| `kaggle_solutions_stats` | 717 场比赛、4724 条档案链接、21 张方法卡 |
| `kaggle_solutions_search` | recommender 查询返回 2 个比赛结果 |
| `kaggle_solutions_show` | 取得 `otto-recommender-system` 比赛档案 |
| `kaggle_solutions_patterns` | retrieval 查询返回 3 张方法卡 |
| `kaggle_research_scenarios` | OTTO、BirdCLEF 2024、ROGII、AmEx、M5 五个真实历史场景 |
| `kaggle_research_plan` | OTTO 研究计划写入指定本机 workspace，生成 5 个角色任务，`dispatch_status: not_dispatched` |

原始工具结果保存在维护者本机的忽略目录 `cache/harness-local-tool-results.json`，其中只有离线档案、方法卡与研究计划数据。临时验证插件不在发行包内，完成后已从专用 profile 的后续启动配置移除。

## 凭据与验证边界

首次旧版 Harness 启动在加载用户现有凭据文件时失败：旧版 provider 要求所有凭据值为字符串，但现有文件包含非字符串 `version` 字段。该错误发生于研究插件激活之前。

维护过程中没有改写用户现有凭据文件。只在专用测试 profile 覆盖 `credentials.path` 为该 profile 的空测试凭据文件，随后完成 Web host 及六个离线工具调用。验证不需要读取或输出用户 token/API key。

浏览器实际打开该本机 Web host，在设置 → 插件 → 插件列表中搜索 `kaggle`，查到模块 `kaggle-solutions-skills/deepseek-harness`，状态为已挂载、已启用。下面是实际设置窗口截图。旧版界面显示模块名，未显示导出的双语标题与自定义图标。

![本机 Harness 插件已挂载、已启用](assets/harness-plugin.png)

因此，这份记录证明 **本机旧版 Harness 的实际安装、完整 host 启动、研究工具调用和插件管理 UI 状态**；它不证明模型登录、付费模型对话、角色实际派发、比赛训练或 Kaggle 官方成绩。另一次真实多 Agent 研究验证见 [OTTO 试用](examples/otto-team-run.md)，执行宿主为 Codex。

另外，自动测试已使用官方发布的 `@deepseek-ai/dsh-tools@0.2.0-rc.2`、`@deepseek-ai/cordis@4.0.4` 与 `SystemPrompt` 验证加载、查询执行、错误传播和卸载清理。两种验证分别覆盖用户当前旧版完整 host 与新版官方 npm 工具运行时，不能推广为所有版本兼容。

## 插件发现与社区目录

[DeepSeek Harness 官方 README](https://github.com/deepseek-ai/deepseek-harness#community-and-support) 指定 GitHub `dsh-plugin` topic 作为插件发现渠道。目前查到的 [1024Store](https://github.com/imsai-sh/awesome-deepseek-harness-plugins) 是社区目录与商店，其静态收录流程不是官方运行认证。

其 [贡献规范](https://github.com/imsai-sh/awesome-deepseek-harness-plugins/blob/main/CONTRIBUTING.md) 允许提交一个 `catalog/plugins/*.json` 条目；通过后自动同步目录。没有 npmjs 发布的插件仍可收录为浏览条目，商店安装命令需要公开 npm registry 的 latest manifest 包含 `dsh.bundle`。GitHub Packages 和公开 Release tarball 的下载能力应与社区商店的安装状态分别说明。
