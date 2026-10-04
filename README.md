<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Kaggle solutions to reusable intelligence: discover, read, distill, validate" width="100%">
</p>

<h1 align="center">kaggle-solutions-skills</h1>

<p align="center">
  <strong>从历史解法中找到思路，把真实证据积累成可复用的 Skill。</strong><br>
  有来源 · 可检索 · 可迁移 · 持续维护
</p>

<p align="center">
  <a href="https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/tag/v0.1.1"><img src="https://img.shields.io/badge/version-0.1.1-2563eb?style=flat-square" alt="Version 0.1.1"></a>
  <a href="#quick-start"><img src="https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&amp;logo=python&amp;logoColor=white" alt="Python 3.10 or newer"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-10b981?style=flat-square" alt="MIT license"></a>
  <a href="https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/workflows/ci.yml"><img src="https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/workflows/ci.yml/badge.svg" alt="Skill checks CI"></a>
  <a href="#coverage"><img src="https://img.shields.io/badge/archive-717%20competitions-0ea5e9?style=flat-square" alt="Snapshot: 717 competitions"></a>
  <a href="#coverage"><img src="https://img.shields.io/badge/reviewed-21%20method%20cards-8b5cf6?style=flat-square" alt="Snapshot: 21 reviewed method cards"></a>
</p>

<p align="center">
  <a href="#quick-start">快速开始</a> ·
  <a href="#workflow">工作流程</a> ·
  <a href="#coverage">知识覆盖</a> ·
  <a href="docs/examples/rogii-research-brief.md">研究示例</a> ·
  <a href="#maintenance">长期维护</a>
</p>

---

以 [faridrashidi/kaggle-solutions](https://github.com/faridrashidi/kaggle-solutions) 为发现索引，进一步读取作者解法正文与代码，提炼方法的**适用条件、失败风险和最小实验**。面向 Agent，也适合研究者直接检索和阅读。

| 🔎 找到相关解法 | 🧩 提炼可迁移方法 | 🌱 积累长期知识 |
| :--- | :--- | :--- |
| 按关键词与模态检索比赛，定位作者原文和排名线索。 | 保留证据与前提，把历史方案转成目标比赛的实验假设。 | 记录真实实验与反例，审核上游更新，维护可分发的 Skill。 |

<a id="quick-start"></a>

## ⚡ 快速开始

### 1. 一条命令安装

需要 **Node.js 20+**。从公开 Release 安装完整 Skill，无需 GitHub token：

```powershell
npx --yes --package=https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.1.1/haoxuanjng-lang-kaggle-solutions-skills-0.1.1.tgz kaggle-solutions-skills install
```

已有安装可追加 `--force` 更新；`--destination <skill-folder>` 可指定目录。

📦 [GitHub Packages](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/packages) · [下载 npm 安装包](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.1.1/haoxuanjng-lang-kaggle-solutions-skills-0.1.1.tgz) · [下载 Skill ZIP](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.1.1/kaggle-solutions-skills-0.1.1.zip)

<details>
<summary><strong>从源码安装 / 使用 GitHub npm registry</strong></summary>

需要 **Python 3.10+**。离线 `search` / `show` / `patterns` 只使用标准库；开发安装会提供更新与校验所需的 PyYAML。

```powershell
git clone https://github.com/haoxuanjng-lang/kaggle-solutions-skills.git
cd kaggle-solutions-skills
python -m pip install -e .
python scripts/project.py install
```

GitHub Packages 的 npm 包为 `@haoxuanjng-lang/kaggle-solutions-skills`，发布在 `npm.pkg.github.com`。按 [GitHub 官方说明](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry) 完成 registry 认证后：

```powershell
npx --yes --registry=https://npm.pkg.github.com @haoxuanjng-lang/kaggle-solutions-skills@0.1.1 install
```

普通下载与安装可直接使用上方 Release 命令，无需配置 registry。Python 3.10+ 用于运行 Skill 内的研究工具；Node.js 只负责安装文件。

</details>

安装后，在新聊天中调用：

```text
$kaggle-solutions-skills 为这场比赛查找类似问题和解法，提炼有依据的实验方向。
```

### 2. 检索知识

```powershell
# 查看当前档案与研究覆盖
python skills/kaggle-solutions-skills/scripts/solutions.py stats

# 搜索相似问题
python skills/kaggle-solutions-skills/scripts/solutions.py search "医学影像" --modality vision --limit 5

# 查看指定比赛的解法线索
python skills/kaggle-solutions-skills/scripts/solutions.py show rogii-wellbore-geology-prediction --top-rank 5 --json

# 查询可迁移方法
python skills/kaggle-solutions-skills/scripts/solutions.py patterns "蒸馏" --json
```

### 3. 从研究走向实验

| 你想完成的事 | 可以这样调用 |
| :--- | :--- |
| 比较历史方案 | `$kaggle-solutions-skills 比较 OTTO 冠军的候选召回和排序策略，给出最小对照实验。` |
| 沉淀比赛经验 | `$kaggle-solutions-skills 把我这次实验的成功与失败整理为方法卡，保留真实结果。` |
| 更新知识库 | `$kaggle-solutions-skills 更新解法索引，审核上游变化并检查安装版本。` |

📖 [阅读 Skill 入口](skills/kaggle-solutions-skills/SKILL.md) · [查看 ROGII 研究交接示例](docs/examples/rogii-research-brief.md)

<details>
<summary><strong>安装位置与 ZIP 分发</strong></summary>

默认安装到 `$CODEX_HOME/skills/kaggle-solutions-skills`；未设置时为 `~/.codex/skills/kaggle-solutions-skills`。可用 `python scripts/project.py install --destination <skill-folder>` 指定位置。

安装只复制 Skill 及离线知识；缓存、上游 checkout 和私人比赛文件留在源项目。

```powershell
python scripts/project.py package
```

导出 ZIP 包含 Skill、离线知识、MIT 与上游许可，并校验 CRC 和文件字节。也可从 [Releases](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases) 获取已发布版本。

</details>

<a id="workflow"></a>

## 🧭 工作流程

![从比赛问题到方法卡、实验交接与知识回流的工作流程](docs/assets/research-workflow.svg)

| 阶段 | 产出 | 需要保留的依据 |
| :--- | :--- | :--- |
| **检索** | 相似比赛与候选解法 | 比赛、链接、排名线索、上游版本 |
| **阅读** | 原文与代码证据 | 作者表述、代码位置、访问状态 |
| **提炼** | 有条件的方法卡 | 适用前提、失败条件、来源关联 |
| **交接** | 最小对照实验 | 目标假设、验证方式、资源约束 |
| **回流** | 新证据与反例 | 实际结果、运行环境、版本 |

真正训练、运行和取得 Kaggle 官方分数时，将研究结果交给用户选定的比赛 workflow；已有 `agentic-kaggle-skill` 时按它执行。

> **证据边界**：档案链接、作者报告、迁移假设、本地实验和官方分数分别记录。历史排名可以帮助发现解法；目标比赛中的收益需要实际验证。

<a id="coverage"></a>

## 📚 知识覆盖

**v0.1.0 · 2026-10-04 导入快照**。档案与方法卡徽章及下表均为本版本的固定统计；更新后的实时数量以 `stats` 输出为准。

| 档案索引 | 已阅读资料 | 已审核知识 |
| :--- | :--- | :--- |
| **717** 场比赛 | **13** 篇解法正文 | **21** 张方法卡 |
| **4,724** 条解法链接记录 | **1** 份作者代码 README（Santa 2024） | 作者报告与待验证的迁移假设 |
| **4,708** 个不同 URL | **7** 份 Skill 设计参考文件，来自 **6** 个 GitHub 项目 | 适用条件、失败风险与来源关联 |

部分已读正文只提供局部方法或指向代码；125 场比赛暂无解法链接。上述数量表示档案与研究覆盖，4,708 个 URL 的可访问性、正文阅读和复现状态仍需逐项确认。本项目尚未运行这些冠军训练方案。

<details>
<summary><strong>查看快照来源与可追溯记录</strong></summary>

上游仓库：[faridrashidi/kaggle-solutions](https://github.com/faridrashidi/kaggle-solutions)。

固定上游版本：[`6414951ae88d252a6c92d4489ba389b2b7cb40c7`](https://github.com/faridrashidi/kaggle-solutions/commit/6414951ae88d252a6c92d4489ba389b2b7cb40c7)。

- [本版本验证记录](docs/validation.md)
- [知识字段与证据状态](skills/kaggle-solutions-skills/references/knowledge-schema.md)
- [来源与第三方许可](THIRD_PARTY_NOTICES.md)

</details>

## 📥 读取解法正文

可选择现有浏览器、MCP、官方 CLI，或安装本项目的可选读取依赖：

```powershell
python -m pip install -e ".[kaggle-read]"
python skills/kaggle-solutions-skills/scripts/fetch_source.py https://www.kaggle.com/competitions/birdclef-2024/discussion/512197 --cache cache/sources
```

读取工具使用现有 API token，不打印或写出凭据。Modern writeup 和旧论坛正文分别处理，并验证取得的是原帖。它不提交、不上传、不启动云端 notebook。Kaggle 内部读取接口可能变化；访问失败会留下明确状态，应转到其他读取方式。

<a id="maintenance"></a>

## 🌱 长期维护

**上游持续更新，方法卡逐条审核，实际实验持续回流。** 项目版本与上游快照版本分开记录。

| 维护机制 | 当前行为 |
| :--- | :--- |
| [持续集成](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/workflows/ci.yml) | 检查结构、来源关联、索引一致性和脚本行为；覆盖 Windows / Ubuntu 与 Python 3.11 / 3.13。 |
| [上游更新检查](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/workflows/sync-upstream.yml) | 每周一北京时间 **09:00** 检查，有新 commit 时生成 review PR；支持手动运行。 |
| 人工知识维护 | 阅读正文与代码 → 条件化方法卡 → 目标比赛假设 → 实际实验 → 补充反例或扩大适用范围。 |

同步 PR 不自动合并，不覆盖人工方法卡，也不更新本地安装副本。定时运行受 GitHub Actions 配额、仓库权限与服务调度影响。

<details>
<summary><strong>维护命令</strong></summary>

```powershell
python skills/kaggle-solutions-skills/scripts/solutions.py refresh
python skills/kaggle-solutions-skills/scripts/solutions.py validate
python -m unittest discover -s tests -v
python scripts/project.py check
python scripts/project.py install
```

</details>

### 项目结构

```text
kaggle-solutions-skills/
├── skills/kaggle-solutions-skills/   # 可安装与分发的 Skill
│   ├── SKILL.md                     # Agent 入口与研究流程
│   ├── references/                  # 知识、来源与维护约定
│   └── scripts/                     # 检索、校验与正文读取
├── docs/                           # 示例、路线与验证记录
├── scripts/project.py              # 项目检查、安装与打包
├── tests/                          # 脚本行为检查
└── .github/workflows/               # CI 与上游更新检查
```

## 🤝 参与维护

欢迎补充可追溯的解法资料、方法适用条件、失败案例与实际实验结果。提交前请阅读 [贡献约定](CONTRIBUTING.md) 和 [维护流程](skills/kaggle-solutions-skills/references/maintenance.md)。

| 开始贡献 | 了解方向 | 查看演进 |
| :--- | :--- | :--- |
| [CONTRIBUTING](CONTRIBUTING.md) | [Roadmap](docs/roadmap.md) | [Changelog](CHANGELOG.md) |

---

<p align="center">
  基于 <a href="https://github.com/faridrashidi/kaggle-solutions">Farid Rashidi 的 Kaggle 解法档案</a>，感谢解法作者的公开分享。<br>
  核心代码与新写指令采用 <a href="LICENSE">MIT</a>；上游档案保留原 MIT 许可，链接内容遵循各自许可。<br>
  <sub>独立维护的社区项目 · 非 Kaggle 官方项目</sub>
</p>
