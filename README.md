# kaggle-solutions-skills

把 Kaggle 历史解法变成 **有来源、可检索、可迁移、能持续积累** 的 agent skill。

本项目以 [faridrashidi/kaggle-solutions](https://github.com/faridrashidi/kaggle-solutions)
为发现索引，进一步读取作者解法正文，提炼决策和失败条件。它支持研究、方法对比、实验方向与知识维护。
真正训练、运行和取得 Kaggle 官方分数时，研究结果交给用户选定的比赛 workflow；已有
`agentic-kaggle-skill` 时按它执行。

## 当前版本：0.1.0

2026-10-04 导入的上游快照：

| 内容 | 覆盖 |
|---|---|
| 比赛 | 717 |
| 解法链接记录 / 不同 URL | 4,724 / 4,708 |
| 暂无解法链接的比赛 | 125 |
| 已读解法正文 | 13 篇；部分正文只提供局部方法或指向代码 |
| 已读作者代码 README | 1 份（Santa 2024） |
| skill 设计参考文件 | 7 份，来自 6 个 GitHub 项目 |
| 人工审核方法卡 | 21 张 |
| 上游版本 | `6414951ae88d252a6c92d4489ba389b2b7cb40c7` |

以上是档案覆盖与研究覆盖，不表示 4,708 个链接都已读、仍可访问或已复现。
种子方法卡全部属于作者报告及尚待验证的迁移假设；本项目没有运行这些冠军训练方案。
更新后的实时数量以 `stats` 输出为准。

## 使用

Python 3.10+。离线 `search` / `show` / `patterns` 只使用标准库。
更新、知识校验和项目开发安装 PyYAML：

```powershell
python -m pip install -e .
python skills/kaggle-solutions-skills/scripts/solutions.py stats
python skills/kaggle-solutions-skills/scripts/solutions.py search "医学影像" --modality vision --limit 5
python skills/kaggle-solutions-skills/scripts/solutions.py show rogii-wellbore-geology-prediction --top-rank 5 --json
python skills/kaggle-solutions-skills/scripts/solutions.py patterns "蒸馏" --json
```

安装到正常 Codex skills 目录：

```powershell
python scripts/project.py install
```

可分发的 skill ZIP 可通过 `python scripts/project.py package` 生成。导出包包含 skill 与离线知识、
MIT/上游许可；CRC 和文件字节会校验。项目维护文档与缓存留在源项目。

默认位置为 `$CODEX_HOME/skills/kaggle-solutions-skills`；未设置时为
`~/.codex/skills/kaggle-solutions-skills`。可通过 `--destination <skill-folder>` 指定其他位置。
该命令只复制 skill，包含离线知识，不复制缓存、上游 checkout 或私人比赛文件。
新聊天中可以使用：

```text
$kaggle-solutions-skills 为这场比赛查找类似问题和解法，提炼有依据的实验方向。
$kaggle-solutions-skills 比较 OTTO 冠军的候选召回和排序策略，给出最小对照实验。
$kaggle-solutions-skills 把我这次实验的成功与失败整理为方法卡，保留真实结果。
$kaggle-solutions-skills 更新解法索引，审核上游变化并检查安装版本。
```

Skill 入口：[SKILL.md](skills/kaggle-solutions-skills/SKILL.md)。
一个实际研究交接示例：[ROGII 简报](docs/examples/rogii-research-brief.md)。

## 读取解法正文

可选择现有浏览器/MCP/官方 CLI，或安装本项目的可选读取依赖：

```powershell
python -m pip install -e ".[kaggle-read]"
python skills/kaggle-solutions-skills/scripts/fetch_source.py https://www.kaggle.com/competitions/birdclef-2024/discussion/512197 --cache cache/sources
```

读取工具使用现有 API token，不打印或写出凭据。Modern writeup 和旧论坛正文分别处理，
并验证取得的是原帖。它不提交、不上传、不启动云端 notebook。
Kaggle 内部读取接口可能变化；访问失败会留下明确状态，应转到其他读取方式。

## 长期维护

```powershell
python skills/kaggle-solutions-skills/scripts/solutions.py refresh
python skills/kaggle-solutions-skills/scripts/solutions.py validate
python -m unittest discover -s tests -v
python scripts/project.py check
python scripts/project.py install
```

GitHub CI 检查结构、来源关联、索引一致性和脚本行为。每周一北京时间 09:00 的上游同步
检查有新 commit 时生成 review PR；不自动合并，不覆盖人工方法卡，不同步本地安装副本。
工作流也可以手动运行。定时运行受 GitHub Actions 配额、仓库权限与服务调度影响。

人工维护闭环：新资料 → 正文/代码证据 → 条件化方法卡 → 目标比赛假设 → 实际实验结果 →
补充反例或扩大适用范围。项目版本和上游快照版本分开记录。

- [贡献约定](CONTRIBUTING.md)
- [维护流程](skills/kaggle-solutions-skills/references/maintenance.md)
- [知识字段](skills/kaggle-solutions-skills/references/knowledge-schema.md)
- [后续路线](docs/roadmap.md)
- [本版本验证记录](docs/validation.md)
- [更新记录](CHANGELOG.md)
- [来源和第三方许可](THIRD_PARTY_NOTICES.md)

核心代码与新写指令采用 MIT；上游档案保留 Farid Rashidi 的 MIT 许可。链接到的第三方内容
仍遵循各自许可。本项目独立维护，不代表 Kaggle 官方。
