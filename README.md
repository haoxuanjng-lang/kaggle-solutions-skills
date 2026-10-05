<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Kaggle solutions to reusable intelligence: discover, read, distill, validate" width="100%">
</p>

<h1 align="center">kaggle-solutions-skills</h1>

<p align="center">
  <strong>English</strong> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.zh-TW.md">繁體中文</a>
</p>

<p align="center">
  <strong>Learn from past solutions. Turn evidence into a reusable agent skill.</strong><br>
  Offline knowledge · Native DeepSeek Harness plugin · Multi-agent research · Ongoing knowledge review
</p>

<p align="center">
  <a href="https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/tag/v0.2.1"><img src="https://img.shields.io/badge/version-0.2.1-2563eb?style=flat-square" alt="Version 0.2.1"></a>
  <a href="#quick-start"><img src="https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&amp;logo=python&amp;logoColor=white" alt="Python 3.10 or newer"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-10b981?style=flat-square" alt="MIT license"></a>
  <a href="https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/workflows/ci.yml"><img src="https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/workflows/ci.yml/badge.svg" alt="Skill checks CI"></a>
  <a href="#coverage"><img src="https://img.shields.io/badge/archive-717%20competitions-0ea5e9?style=flat-square" alt="Snapshot: 717 competitions"></a>
  <a href="#coverage"><img src="https://img.shields.io/badge/reviewed-21%20method%20cards-8b5cf6?style=flat-square" alt="Snapshot: 21 reviewed method cards"></a>
  <a href="#deepseek"><img src="https://img.shields.io/badge/DeepSeek%20Harness-native%20plugin-6366f1?style=flat-square" alt="DeepSeek Harness native plugin"></a>
  <a href="#scenarios"><img src="https://img.shields.io/badge/research-5%20scenarios-0d9488?style=flat-square" alt="Five historical competition research scenarios"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#workflow">Workflow</a> ·
  <a href="#deepseek">DeepSeek plugin</a> ·
  <a href="#team">Agent collaboration</a> ·
  <a href="#scenarios">Competition scenarios</a> ·
  <a href="#coverage">Knowledge coverage</a> ·
  <a href="docs/examples/rogii-research-brief.md">Research example</a> ·
  <a href="#maintenance">Ongoing updates</a>
</p>

---

Kaggle solutions are scattered across discussions, notebooks, and author repositories. After finding a winning solution, you still need to assess its validation, decide what transfers to your data, combine research from several agents, and carry useful lessons into the next competition.

This project uses [faridrashidi/kaggle-solutions](https://github.com/faridrashidi/kaggle-solutions) as a discovery index. It distills author material that has actually been read into method cards with sources and conditions, then gives Codex and DeepSeek Harness access to the same knowledge base. The result: **related solutions, validation risks, and comparable minimal experiments**.

| 🔎 Find relevant solutions | 🧩 Research with multiple agents | 🌱 Build lasting knowledge |
| :--- | :--- | :--- |
| Search competitions by keyword and modality. Reuse the same knowledge through a Codex skill or native Harness tools. | Five roles—scout, evidence, validation, transfer, and synthesis—share sources and unknowns while preserving disagreements. | Review archive and method-card updates. Record actual experiments and counterexamples to improve reusable research knowledge. |

<a id="quick-start"></a>

## ⚡ Quick start

### 1. Install with one command

Requires **Node.js 20+**. Install the complete skill from a public release without a GitHub token:

```powershell
npx --yes --package=https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.2.1/haoxuanjng-lang-kaggle-solutions-skills-0.2.1.tgz kaggle-solutions-skills install
```

Add `--force` to update an existing installation, or `--destination <skill-folder>` to choose a directory.

📦 [GitHub Packages](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/packages) · [Download the npm package](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.2.1/haoxuanjng-lang-kaggle-solutions-skills-0.2.1.tgz) · [Download the skill ZIP](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.2.1/kaggle-solutions-skills-0.2.1.zip)

For full installation and release instructions, see [Distribution](docs/distribution.md).

<details>
<summary><strong>Install from source / use the GitHub npm registry</strong></summary>

Requires **Python 3.10+**. Offline `search` / `show` / `patterns` use only the standard library. The development installation also provides PyYAML for updates and validation.

```powershell
git clone https://github.com/haoxuanjng-lang/kaggle-solutions-skills.git
cd kaggle-solutions-skills
python -m pip install -e .
python scripts/project.py install
```

The npm package is `@haoxuanjng-lang/kaggle-solutions-skills`, published at `npm.pkg.github.com`. After configuring registry authentication according to the [official GitHub instructions](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry):

```powershell
npx --yes --registry=https://npm.pkg.github.com @haoxuanjng-lang/kaggle-solutions-skills@0.2.1 install
```

For ordinary downloads and installation, use the public release command above without configuring a registry. Python 3.10+ runs the skill's research tools; Node.js installs the files.

</details>

After installation, invoke the skill in a new chat:

```text
$kaggle-solutions-skills Find similar problems and solutions for this competition, and propose experiments supported by evidence.
```

### 2. Search the knowledge base

The commands below run from the source checkout. For an installed skill, use the corresponding script paths under its installation directory.

```powershell
# Inspect archive and research coverage
python skills/kaggle-solutions-skills/scripts/solutions.py stats

# Search for similar problems (medical imaging)
python skills/kaggle-solutions-skills/scripts/solutions.py search "medical imaging" --modality vision --limit 5

# Inspect solution leads for a competition
python skills/kaggle-solutions-skills/scripts/solutions.py show rogii-wellbore-geology-prediction --top-rank 5 --json

# Look up transferable methods (distillation)
python skills/kaggle-solutions-skills/scripts/solutions.py patterns "distillation" --json
```

### 3. Turn research into experiments

| Your goal | Example prompt |
| :--- | :--- |
| Compare historical approaches | `$kaggle-solutions-skills Compare candidate retrieval and ranking in the OTTO winning solution, and propose a minimal controlled experiment.` |
| Preserve competition lessons | `$kaggle-solutions-skills Turn successes and failures from my experiment into method cards, preserving the actual results.` |
| Update the knowledge base | `$kaggle-solutions-skills Update the solution index, review upstream changes, and check the installed version.` |

📖 [Read the skill entry point](skills/kaggle-solutions-skills/SKILL.md) · [See the ROGII research handoff example](docs/examples/rogii-research-brief.md)

<details>
<summary><strong>Installation directory and ZIP distribution</strong></summary>

The default destination is `$CODEX_HOME/skills/kaggle-solutions-skills`, or `~/.codex/skills/kaggle-solutions-skills` when the variable is unset. Use `python scripts/project.py install --destination <skill-folder>` to choose a location.

Installation copies only the skill and offline knowledge. Caches, upstream checkouts, and private competition files stay in the source project.

```powershell
python scripts/project.py package
```

The ZIP includes the skill, offline knowledge, MIT license, and upstream license. Packaging verifies CRC and file bytes. Published versions are also available from [Releases](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases).

</details>

<a id="workflow"></a>

## 🧭 Workflow

![Workflow from a competition question to method cards, experiment handoffs, and knowledge feedback](docs/assets/research-workflow.svg)

| Stage | Output | Evidence to preserve |
| :--- | :--- | :--- |
| **Discover** | Similar competitions and candidate solutions | Competition, links, rank leads, and upstream version |
| **Read** | Evidence from original material and code | Author statements, code locations, and access status |
| **Distill** | Method cards with conditions | Prerequisites, failure conditions, and source references |
| **Hand off** | Minimal controlled experiments | Target hypothesis, validation design, and resource limits |
| **Feed back** | New evidence and counterexamples | Actual results, runtime environment, and version |

For training, execution, and official Kaggle scores, pass the research to the user's chosen competition workflow. When `agentic-kaggle-skill` is already in use, follow it.

> **Evidence boundaries:** Archive links, author reports, transfer hypotheses, local experiments, and official scores are recorded separately. Historical ranks help discover solutions; benefits in the target competition require actual validation.

<a id="deepseek"></a>

## 🐋 Native DeepSeek Harness plugin

### Current pain points and what the plugin helps you do

| Current pain point | How Harness helps | Deliverable |
| :--- | :--- | :--- |
| Many solutions are available, but their relevance to the current problem is unclear. | Search by problem, modality, and historical competition, then inspect solution leads. | Related competitions, author sources, and items to verify |
| Winning solutions contain many techniques; transfer can overlook validation and data boundaries. | Query method cards with conditions, then have evidence and validation agents investigate separately. | Preconditions, leakage risks, failure conditions, and minimal controls |
| Agents repeat searches, lose context, or mix author reports with actual experiments when merging results. | Generate separate task packets, a dependency graph, and source context for reviewer synthesis. | Research handoffs, unresolved disagreements, and experiment proposals |

Ask Harness to find similar problems for a new competition, compare solutions, organize a research team, or preserve feedback from actual experiments. Offline retrieval and task generation work directly. New model analysis uses your Harness configuration; experiments and official scores come from the competition execution workflow.

The same npm package includes the Cordis plugin, bundle patch, bilingual metadata, and tool icon. All six tools were successfully called in a local **Harness `0.1.0-rc.6` full Web host**, with the plugin manager showing the plugin mounted and enabled. The official **`0.2.0-rc.2` tool runtime** was also used to verify registration, execution, error propagation, and disposal. See the [local validation record and screenshot](docs/harness-local-validation.md).

Download the `.tgz` from the [release](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/tag/v0.2.1), then run these commands in the directory containing it:

```bash
npx @deepseek-ai/dsh@0.2.0-rc.2 plugin --profile kaggle add ./haoxuanjng-lang-kaggle-solutions-skills-0.2.1.tgz
npx @deepseek-ai/dsh@0.2.0-rc.2 --profile kaggle --dump-config
```

| Retrieval tools | Evidence tools | Collaboration tools |
| :--- | :--- | :--- |
| `kaggle_solutions_search` | `kaggle_solutions_show` | `kaggle_research_scenarios` |
| `kaggle_solutions_stats` | `kaggle_solutions_patterns` | `kaggle_research_plan` |

Offline tools need no additional API key. Model conversations use Harness's own configuration. The plugin generates task packets; actual dispatch uses the host's subagent or workflow capabilities. Official Harness remains in developer preview. See the [plugin guide](docs/deepseek-harness.md) for compatibility and workspace configuration.

Community discovery: listed in [1024Store](https://deepseek1024.com/plugins/haoxuanjng-lang/kaggle-solutions-skills) ([merged catalog PR](https://github.com/imsai-sh/awesome-deepseek-harness-plugins/pull/567)). This is a community directory, not DeepSeek official certification. Use the verified Release tarball above for installation.

<a id="team"></a>

## 🤖 Multi-agent research

![Dependency graph and evidence handoffs for the five-role research team](docs/assets/agent-team.svg)

```powershell
python skills/kaggle-solutions-skills/scripts/research_team.py plan --scenario otto --output workspaces/otto-research
python skills/kaggle-solutions-skills/scripts/research_team.py validate workspaces/otto-research
```

Each role receives its own task, pinned source context, result contract, and paths to prerequisite outputs. Evidence reading and validation review can run in parallel. Transfer analysis waits for both, and the reviewer combines traceable findings, disagreements, and minimal experiments.

In Codex, ask directly:

```text
$kaggle-solutions-skills Use multiple agents to analyze OTTO retrieval and ranking, review validation leakage, and propose minimal transfer experiments. Keep missing target metrics unknown.
```

**Generating task packets does not mean agents have run.** After execution by the host, use `validate <research-directory> --results` to check role outputs and source references. A valid format still requires a researcher to assess whether sources support the claims. [Collaboration workflow](skills/kaggle-solutions-skills/references/multi-agent-research.md) · [Research usage guide](docs/examples/team-research.md)

An [actual OTTO research trial](docs/examples/otto-team-run.md) completed all five roles in dependency order. Independent evidence and validation agents ran in parallel, read cached author material, and contributed to a transfer experiment brief. This record validates the research workflow; competition gains remain unverified.

Archive facts now cite their own pinned source ID with `archive_metadata`; author observations keep their author source IDs. The validator rejects mixing these claim types. See the [citation contract](skills/kaggle-solutions-skills/references/multi-agent-research.md#archive-and-author-citations).

<a id="scenarios"></a>

## 🏁 Research scenarios from real competitions

| Scenario ID | Original competition | Research focus | Minimal experiment direction |
| :--- | :--- | :--- | :--- |
| `otto` | [OTTO](https://www.kaggle.com/competitions/otto-recommender-system) | Session boundaries, candidate retrieval, and ranking | Hold candidate generation fixed; compare only the ranking stage |
| `birdclef-2024` | [BirdCLEF 2024](https://www.kaggle.com/competitions/birdclef-2024) | Audio context, source quality, and pseudolabel isolation | Change one context or pseudolabel strategy with the same split and budget |
| `rogii` | [ROGII](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction) | Cross-well validation, alignment, and reliability routing | Hold the baseline fixed; compare one alignment or routing change |
| `amex` | [American Express](https://www.kaggle.com/competitions/amex-default-prediction) | Customer isolation, historical features, and metric alignment | Preserve the customer split; add one group of historical statistical features |
| `m5` | [M5](https://www.kaggle.com/competitions/m5-forecasting-accuracy) | Forecast horizons, recursive inference, and hierarchical metrics | Compare direct and recursive forecasts with the same horizon and training cost |

The five scenarios connect real competitions with author material recorded as read and with method cards. They support research and collaboration regression checks. These are **historical solution research scenarios**; this project has not reproduced their winning training pipelines or produced new official scores.

```powershell
python skills/kaggle-solutions-skills/scripts/research_team.py scenarios --json
```

<a id="coverage"></a>

## 📚 Knowledge coverage

**v0.1.0 · Imported snapshot dated 2026-10-04.** The archive and method-card badges and table below show fixed snapshot counts. For current counts after updates, use `stats`.

| Archive index | Material actually read | Reviewed knowledge |
| :--- | :--- | :--- |
| **717** competitions | **13** solution writeups | **21** method cards |
| **4,724** solution-link records | **1** author code README (Santa 2024) | Author reports and transfer hypotheses awaiting validation |
| **4,708** distinct URLs | **7** skill-design reference files from **6** GitHub projects | Preconditions, failure risks, and source references |

Some read material covers only part of a method or points to code. Another 125 competitions have no solution links. These counts describe archive and research coverage. Access, reading, and reproduction status for the 4,708 URLs still require individual verification. This project has not run these winning training pipelines.

<details>
<summary><strong>Inspect snapshot provenance and traceable records</strong></summary>

Upstream repository: [faridrashidi/kaggle-solutions](https://github.com/faridrashidi/kaggle-solutions).

Pinned upstream revision: [`6414951ae88d252a6c92d4489ba389b2b7cb40c7`](https://github.com/faridrashidi/kaggle-solutions/commit/6414951ae88d252a6c92d4489ba389b2b7cb40c7).

- [Version validation record](docs/validation.md)
- [Knowledge fields and evidence states](skills/kaggle-solutions-skills/references/knowledge-schema.md)
- [Sources and third-party licenses](THIRD_PARTY_NOTICES.md)

</details>

## 📥 Read solution material

Use an existing browser, MCP, or official CLI, or install this project's optional reading dependencies:

```powershell
python -m pip install -e ".[kaggle-read]"
python skills/kaggle-solutions-skills/scripts/fetch_source.py https://www.kaggle.com/competitions/birdclef-2024/discussion/512197 --cache cache/sources
```

The reader uses an existing API token without printing or exporting credentials. It handles modern writeups and legacy forum posts separately and checks that the retrieved content is the original post. It does not submit, upload, or start cloud notebooks. Kaggle's internal reading interfaces may change; access failures leave an explicit status so you can switch to another reader.

<a id="maintenance"></a>

## 🌱 Ongoing updates and knowledge review

The project tracks changes in the upstream solution archive, reviews index updates, and improves method cards using author material and evidence from actual experiments. Project versions and upstream snapshots are recorded separately. Updates preserve existing method cards and do not automatically overwrite an installed skill.

See the [Changelog](CHANGELOG.md) and [Releases](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases) for updates. Add `--force` to the installation command to update an existing installation. See the [maintenance documentation](docs/daily-maintenance.md) for maintenance mechanisms, scheduling, and configuration.

### Project structure

```text
kaggle-solutions-skills/
├── skills/kaggle-solutions-skills/   # Installable and distributable skill
│   ├── SKILL.md                     # Agent entry point and research workflow
│   ├── references/                  # Knowledge, sources, and maintenance conventions
│   └── scripts/                     # Search, validation, and source reading
├── docs/                           # Examples, roadmap, and validation records
├── integrations/deepseek-harness/   # Native plugin, bundle, and bilingual resources
├── config/daily-agent-prompt.md     # Authorized daily project maintenance instructions
├── scripts/project.py              # Project checks, installation, and packaging
├── tests/                          # Script behavior checks
└── .github/workflows/               # CI and upstream update checks
```

## 🤝 Contribute

Contributions of traceable solution material, method conditions, failure cases, and actual experiment results are welcome. Read the [contribution guidelines](CONTRIBUTING.md) and [maintenance workflow](skills/kaggle-solutions-skills/references/maintenance.md) before submitting changes.

| Start contributing | Explore priorities | Follow changes |
| :--- | :--- | :--- |
| [CONTRIBUTING](CONTRIBUTING.md) | [Roadmap](docs/roadmap.md) | [Changelog](CHANGELOG.md) |

---

<p align="center">
  Built on <a href="https://github.com/faridrashidi/kaggle-solutions">Farid Rashidi's Kaggle solutions archive</a>, with thanks to the authors who shared their solutions.<br>
  Core code and newly written instructions use <a href="LICENSE">MIT</a>; the upstream archive retains its original MIT license, and linked content keeps its own license.<br>
  <sub>Independently maintained community project · Not an official Kaggle project</sub>
</p>
