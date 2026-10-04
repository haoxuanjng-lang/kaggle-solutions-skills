# 每日更新与维护

项目维护分为云端检查、上游档案审核和本地 AI 开发。三者的运行证据分别记录，定时检查成功不表示新功能已经开发，也不表示赢得比赛。

| 任务 | 计划时间 | 实际行为 | 依赖与结果 |
|---|---|---|---|
| GitHub `Daily maintenance` | 每天 09:00，Asia/Shanghai | 项目完整性、Python 测试、npm 安装器与打包检查、五个真实比赛研究场景的计划生成与验证 | GitHub Actions；保留报告 14 天，失败显示为 failed |
| GitHub `Review upstream archive` | 每天 09:00，Asia/Shanghai | 查询 `faridrashidi/kaggle-solutions` 的上游 commit；有新 commit 时验证后创建审核 PR | GitHub Actions token 需要创建 PR 的权限；不自动合并 |
| 本地 Codex AI 维护 | 每天 09:00，Asia/Shanghai | 在已授权的本地维护环境研究来源、选择改进、开发测试并更新文档 | 需要电脑开机、用户会话与 Codex/GitHub 认证可用；具体执行记录见本地任务日志 |

GitHub 的这两个 cron 使用 UTC，配置 `0 1 * * *` 对应上海时间 09:00。平台调度可能延迟；公开仓库 60 天没有活动时，定时工作流会被停用。可以在 Actions 中手动运行两个工作流，查看每次的实际开始时间及结果。[GitHub 调度说明](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

## 云端检查覆盖什么

`scripts/daily_maintenance.py` 执行完整性检查、现有 Python/npm 行为测试与 npm 打包预览，然后通过 `research_team.py` 生成并验证 OTTO、BirdCLEF 2024、ROGII、AmEx 与 M5 的研究任务包。任务包在临时目录创建，结束后清理；报告保留检查名称、退出状态与耗时，不保留模型凭据或研究私有材料。

这些场景使用真实比赛的历史研究资料，检验任务分解与交接格式。云端维护没有调用模型、训练、下载比赛数据或提交 Kaggle，因此不声称完成了这些比赛或取得新成绩。

某项检查失败后继续收集其他检查结果，最终仍以非零退出状态标记运行失败。计划生成失败时，对应验证项明确标记 blocked，不能把跳过算作通过。报告写入 Actions 的 Step Summary，同时上传 `report.json` 和 `summary.md`。安装环境失败会直接显示在 Actions 日志中，此时不会伪造检查报告。

```powershell
python -m pip install -e .
python scripts/daily_maintenance.py --output cache/daily-maintenance
```

## 上游变化与知识维护

上游 commit 没变时不创建 issue 或 PR。同一个已创建审核 PR 的 commit 不再重复创建。新的元数据在独立分支更新，原有 `patterns.json` / `sources.json` 保留，结构与行为检查通过后才创建 PR。维护者审核差异后决定合并；新增链接仍然是未读链接，不自动升级为已阅读或已复现。

方法卡与新功能需要阅读来源、记录适用条件、实际修改和相应验证。本地 AI 维护可以承担这项工作；云端定时脚本只执行明确、可重复的检查和元数据审核。外部页面和作者代码均视为研究资料，不能改变维护授权或执行指令。

常规运行无变化时只保留 Actions 记录，不创建每日汇报 issue。失败、需要人工输入或有可审核改进时才产生需要处理的结果。两类 GitHub 工作流均支持 `workflow_dispatch`，可以手动验证配置和恢复运行。

相关文件：[上游审核工作流](../.github/workflows/sync-upstream.yml)、[每日检查工作流](../.github/workflows/daily-maintenance.yml)、[维护脚本](../scripts/daily_maintenance.py)、[维护原则](../skills/kaggle-solutions-skills/references/maintenance.md)。

## 本机 Codex 定时开发

本机任务名为 `Kaggle-Solutions-Skills-Daily-Agent`。Windows 计划任务每天北京时间 09:00 启动隐藏的 Python runner；用户必须已登录，电脑需开机，网络、Codex 订阅额度和 GitHub 认证也需可用。错过计划时间后会在条件满足时补跑；同一个任务不重叠运行。

```powershell
# 检查命令与路径，不运行模型
python scripts/run_daily_agent.py

# 真实模型只读烟测；结果保存在本地日志
python scripts/run_daily_agent.py --smoke

# 注册或更新每日任务；时间为本机上海时区
powershell.exe -NoProfile -File scripts/install_daily_task.ps1 -At 09:00

# 手动执行已授权维护
python scripts/run_daily_agent.py --execute
```

Runner 会 fetch 当前 `origin/main`，创建独立 `maintenance/<timestamp>` 分支与 worktree，将 [维护任务说明](../config/daily-agent-prompt.md) 通过 stdin 交给 `codex exec`。原项目的未提交修改不作为维护输入，也不会被 reset。worktree 与日志留在忽略的 `cache/maintenance/` 目录，便于复查实际改动。

运行记录位于 `cache/maintenance/runs/<timestamp>/`，包含 `status.json`、`runner.log` 和模型写出的 `report.md`。退出成功只代表本次 Codex 执行成功；具体功能、PR、CI 与发布成果以报告链接及实际状态为准。额度不足、认证失败或模型不兼容会记录失败，不伪造每日更新。

任务使用 `--ignore-user-config` 保留登录认证、采用 CLI 支持的默认模型，避免个人配置中的不兼容模型导致无人值守失败；项目 `AGENTS.md` 仍适用。runner 为已授权项目维护提供文件与网络访问，任务说明将范围限定为本项目。权限不延伸到比赛提交、私有数据上传或其他仓库。

可用 `Get-ScheduledTask -TaskName Kaggle-Solutions-Skills-Daily-Agent` 查看注册状态；暂停时执行 `Disable-ScheduledTask`，恢复用 `Enable-ScheduledTask`。该任务没有配置外部消息或每日邮件。
