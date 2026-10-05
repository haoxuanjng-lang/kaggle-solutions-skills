<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="從 Kaggle 解法到可重用的研究知識：探索、閱讀、提煉、驗證" width="100%">
</p>

<h1 align="center">kaggle-solutions-skills</h1>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <strong>繁體中文</strong>
</p>

<p align="center">
  <strong>從歷史解法中找到思路，將真實證據累積成可重用的 Skill。</strong><br>
  離線知識庫 · DeepSeek Harness 原生外掛 · 多 Agent 研究 · 持續知識審查
</p>

<p align="center">
  <a href="https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/tag/v0.2.1"><img src="https://img.shields.io/badge/version-0.2.1-2563eb?style=flat-square" alt="版本 0.2.1"></a>
  <a href="#quick-start"><img src="https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&amp;logo=python&amp;logoColor=white" alt="Python 3.10 或更新版本"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-10b981?style=flat-square" alt="MIT 授權"></a>
  <a href="https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/workflows/ci.yml"><img src="https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/workflows/ci.yml/badge.svg" alt="Skill 檢查 CI"></a>
  <a href="#coverage"><img src="https://img.shields.io/badge/archive-717%20competitions-0ea5e9?style=flat-square" alt="快照：717 場比賽"></a>
  <a href="#coverage"><img src="https://img.shields.io/badge/reviewed-21%20method%20cards-8b5cf6?style=flat-square" alt="快照：21 張已審查方法卡"></a>
  <a href="#deepseek"><img src="https://img.shields.io/badge/DeepSeek%20Harness-native%20plugin-6366f1?style=flat-square" alt="DeepSeek Harness 原生外掛"></a>
  <a href="#scenarios"><img src="https://img.shields.io/badge/research-5%20scenarios-0d9488?style=flat-square" alt="五個歷史比賽研究情境"></a>
</p>

<p align="center">
  <a href="#quick-start">快速開始</a> ·
  <a href="#workflow">工作流程</a> ·
  <a href="#deepseek">DeepSeek 外掛</a> ·
  <a href="#team">Agent 協作</a> ·
  <a href="#scenarios">比賽情境</a> ·
  <a href="#coverage">知識涵蓋範圍</a> ·
  <a href="docs/examples/rogii-research-brief.md">研究範例</a> ·
  <a href="#maintenance">持續更新</a>
</p>

---

Kaggle 解法散落在論壇、Notebook 和作者儲存庫中。找到一個冠軍連結之後，還需要判斷驗證方式是否可靠、哪些決策適合目前的資料、幾個 Agent 的研究如何整合，以及下一場比賽如何重用這些經驗。

本專案以 [faridrashidi/kaggle-solutions](https://github.com/faridrashidi/kaggle-solutions) 作為探索索引，將已閱讀的作者資料整理成附有來源與適用條件的方法卡，讓 Codex 與 DeepSeek Harness 使用同一知識庫，提供**相似解法、驗證風險和可比較的最小實驗**。

| 🔎 找到相關解法 | 🧩 透過 Agent 協作研究 | 🌱 累積長期知識 |
| :--- | :--- | :--- |
| 依關鍵字與模態檢索比賽；Codex Skill 與 Harness 原生工具共用同一知識庫。 | 偵察、證據、驗證、遷移、綜合審查五個角色，傳遞來源與未知項，保留分歧。 | 經審查更新檔案與方法卡；記錄實際實驗與反例，逐步改善可重用的研究知識。 |

<a id="quick-start"></a>

## ⚡ 快速開始

### 1. 一行指令安裝

需要 **Node.js 20+**。從公開 Release 安裝完整 Skill，不需要 GitHub token：

```powershell
npx --yes --package=https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.2.1/haoxuanjng-lang-kaggle-solutions-skills-0.2.1.tgz kaggle-solutions-skills install
```

已有安裝可加上 `--force` 更新；`--destination <skill-folder>` 可指定目錄。

📦 [GitHub Packages](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/packages) · [下載 npm 安裝套件](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.2.1/haoxuanjng-lang-kaggle-solutions-skills-0.2.1.tgz) · [下載 Skill ZIP](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.2.1/kaggle-solutions-skills-0.2.1.zip)

完整安裝與後續發布說明：[Distribution](docs/distribution.md)。

<details>
<summary><strong>從原始碼安裝 / 使用 GitHub npm registry</strong></summary>

需要 **Python 3.10+**。離線 `search` / `show` / `patterns` 僅使用標準函式庫；開發安裝會提供更新與驗證所需的 PyYAML。

```powershell
git clone https://github.com/haoxuanjng-lang/kaggle-solutions-skills.git
cd kaggle-solutions-skills
python -m pip install -e .
python scripts/project.py install
```

GitHub Packages 的 npm 套件為 `@haoxuanjng-lang/kaggle-solutions-skills`，發布於 `npm.pkg.github.com`。依 [GitHub 官方說明](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry) 完成 registry 驗證後：

```powershell
npx --yes --registry=https://npm.pkg.github.com @haoxuanjng-lang/kaggle-solutions-skills@0.2.1 install
```

一般下載與安裝可直接使用上方的 Release 指令，不需要設定 registry。Python 3.10+ 用於執行 Skill 內的研究工具；Node.js 僅負責安裝檔案。

</details>

安裝後，在新聊天中呼叫：

```text
$kaggle-solutions-skills 為這場比賽尋找相似問題和解法，提煉有依據的實驗方向。
```

### 2. 檢索知識

```powershell
# 查看目前檔案與研究涵蓋範圍
python skills/kaggle-solutions-skills/scripts/solutions.py stats

# 搜尋相似問題
python skills/kaggle-solutions-skills/scripts/solutions.py search "医学影像" --modality vision --limit 5

# 查看指定比賽的解法線索
python skills/kaggle-solutions-skills/scripts/solutions.py show rogii-wellbore-geology-prediction --top-rank 5 --json

# 查詢可遷移的方法
python skills/kaggle-solutions-skills/scripts/solutions.py patterns "蒸馏" --json
```

### 3. 從研究走向實驗

| 你想完成的事 | 可以這樣呼叫 |
| :--- | :--- |
| 比較歷史方案 | `$kaggle-solutions-skills 比較 OTTO 冠軍的候選召回和排序策略，提出最小對照實驗。` |
| 累積比賽經驗 | `$kaggle-solutions-skills 將我這次實驗的成功與失敗整理為方法卡，保留真實結果。` |
| 更新知識庫 | `$kaggle-solutions-skills 更新解法索引，審查上游變更並檢查安裝版本。` |

📖 [閱讀 Skill 入口](skills/kaggle-solutions-skills/SKILL.md) · [查看 ROGII 研究交接範例](docs/examples/rogii-research-brief.md)

<details>
<summary><strong>安裝位置與 ZIP 發布</strong></summary>

預設安裝至 `$CODEX_HOME/skills/kaggle-solutions-skills`；未設定時為 `~/.codex/skills/kaggle-solutions-skills`。可使用 `python scripts/project.py install --destination <skill-folder>` 指定位置。

安裝僅複製 Skill 及離線知識；快取、上游 checkout 和私人比賽檔案保留在來源專案。

```powershell
python scripts/project.py package
```

匯出的 ZIP 包含 Skill、離線知識、MIT 與上游授權，並驗證 CRC 和檔案位元組。也可從 [Releases](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases) 取得已發布版本。

</details>

<a id="workflow"></a>

## 🧭 工作流程

![從比賽問題到方法卡、實驗交接與知識回流的工作流程](docs/assets/research-workflow.svg)

| 階段 | 產出 | 需要保留的依據 |
| :--- | :--- | :--- |
| **檢索** | 相似比賽與候選解法 | 比賽、連結、排名線索、上游版本 |
| **閱讀** | 原文與程式碼證據 | 作者陳述、程式碼位置、存取狀態 |
| **提煉** | 附有適用條件的方法卡 | 適用前提、失敗條件、來源關聯 |
| **交接** | 最小對照實驗 | 目標假設、驗證方式、資源限制 |
| **回流** | 新證據與反例 | 實際結果、執行環境、版本 |

實際訓練、執行並取得 Kaggle 官方分數時，將研究結果交給使用者選定的比賽 workflow；已有 `agentic-kaggle-skill` 時依其流程執行。

> **證據邊界**：檔案連結、作者報告、遷移假設、本機實驗和官方分數分別記錄。歷史排名可以幫助探索解法；在目標比賽中的效益需要實際驗證。

<a id="deepseek"></a>

## 🐋 DeepSeek Harness 原生外掛

### 目前痛點與外掛能幫你做的事

| 目前痛點 | 在 Harness 中如何解決 | 提供什麼 |
| :--- | :--- | :--- |
| 找到許多方案，難以判斷與目前問題是否相似 | 依問題、模態和歷史比賽檢索，查看對應的解法線索 | 相似比賽、作者來源和待確認項目 |
| 冠軍方案有許多技巧，遷移時容易忽略驗證與資料邊界 | 查詢附有適用條件的方法卡，讓證據 Agent 與驗證 Agent 分別研究 | 適用條件、洩漏風險、失敗條件與最小對照 |
| 多 Agent 重複搜尋、脈絡遺失，彙整時混淆作者報告與實際實驗 | 產生獨立任務包、相依圖和來源脈絡，由 reviewer 綜合審查 | 可交接的研究結果、尚未解決的分歧與實驗建議 |

可以讓 Harness 為新比賽尋找相似問題、比較某場比賽的解法、組織研究團隊，或將實際實驗回饋累積成知識。離線檢索與任務產生可直接使用；新的模型分析沿用你的 Harness 設定，實驗與官方成績由比賽執行 workflow 產生。

同一份 npm 套件包含 Cordis 外掛、bundle patch、雙語中繼資料和工具圖示。已在本機 **Harness `0.1.0-rc.6` 完整 Web host** 中成功呼叫六個工具，外掛管理頁顯示已掛載、已啟用；同時使用官方 **`0.2.0-rc.2` 工具執行環境** 驗證註冊、呼叫、錯誤傳遞與卸載。詳見 [本機驗證紀錄與截圖](docs/harness-local-validation.md)。

從 [Release](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/tag/v0.2.1) 下載 `.tgz` 後，在檔案所在目錄執行：

```bash
npx @deepseek-ai/dsh@0.2.0-rc.2 plugin --profile kaggle add ./haoxuanjng-lang-kaggle-solutions-skills-0.2.1.tgz
npx @deepseek-ai/dsh@0.2.0-rc.2 --profile kaggle --dump-config
```

| 檢索工具 | 證據工具 | 協作工具 |
| :--- | :--- | :--- |
| `kaggle_solutions_search` | `kaggle_solutions_show` | `kaggle_research_scenarios` |
| `kaggle_solutions_stats` | `kaggle_solutions_patterns` | `kaggle_research_plan` |

離線工具不需要額外 API key；模型對話沿用 Harness 自身設定。外掛產生任務包，實際分派使用宿主的 subagent/workflow 功能。官方 Harness 仍處於 developer preview，相容範圍和 workspace 設定詳見 [外掛指南](docs/deepseek-harness.md)。

社群探索：已收錄至 [1024Store](https://deepseek1024.com/plugins/haoxuanjng-lang/kaggle-solutions-skills)（[收錄 PR 已合併](https://github.com/imsai-sh/awesome-deepseek-harness-plugins/pull/567)）。這是社群目錄收錄，不代表 DeepSeek 官方認證。安裝請使用上方已驗證的 Release 套件。

<a id="team"></a>

## 🤖 多 Agent 協作研究

![五角色研究團隊的相依圖與證據交接](docs/assets/agent-team.svg)

```powershell
python skills/kaggle-solutions-skills/scripts/research_team.py plan --scenario otto --output workspaces/otto-research
python skills/kaggle-solutions-skills/scripts/research_team.py validate workspaces/otto-research
```

每個角色取得獨立任務、固定來源脈絡、結果契約和前置結果路徑。證據閱讀與驗證審查可並行進行；遷移分析等待兩者完成，最後由 reviewer 彙整可追溯的發現、分歧和最小實驗。

在 Codex 中可以直接提出：

```text
$kaggle-solutions-skills 使用多 Agent 分析 OTTO 的召回與排序方案，審查驗證洩漏，提出最小遷移實驗。缺少的目標指標保持未知。
```

**任務包已產生 ≠ Agent 已執行。** 宿主實際執行後，透過 `validate <研究目录> --results` 檢查角色結果與來源關聯。格式通過後，仍需要研究者判斷事實是否得到來源支持。[協作流程](skills/kaggle-solutions-skills/references/multi-agent-research.md) · [實際研究使用說明](docs/examples/team-research.md)

已完成一次 [OTTO 真實研究試用](docs/examples/otto-team-run.md)：五個角色依相依關係完成研究，其中 evidence / validation 由獨立 Agent 並行執行，審讀快取的作者正文後輸出遷移實驗簡報。該紀錄驗證研究流程，尚未驗證比賽效益。

檔案事實現在使用獨立的固定版本來源 ID 和 `archive_metadata`；作者觀察保留作者來源 ID。驗證器會拒絕混用這兩類聲明。見[引用契約](skills/kaggle-solutions-skills/references/multi-agent-research.md#archive-and-author-citations)。

<a id="scenarios"></a>

## 🏁 真實比賽研究情境

| 情境 ID | 原比賽 | 研究重點 | 最小實驗方向 |
| :--- | :--- | :--- | :--- |
| `otto` | [OTTO](https://www.kaggle.com/competitions/otto-recommender-system) | Session 邊界、候選召回與排序 | 固定候選產生方式，單獨比較排序階段 |
| `birdclef-2024` | [BirdCLEF 2024](https://www.kaggle.com/competitions/birdclef-2024) | 音訊上下文、來源品質、偽標籤隔離 | 在相同 split 和預算下改變一種上下文或偽標籤策略 |
| `rogii` | [ROGII](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction) | 跨井驗證、對齊與可靠性路由 | 固定基準方案，比較單項對齊或路由變更 |
| `amex` | [American Express](https://www.kaggle.com/competitions/amex-default-prediction) | 客戶隔離、歷史特徵與指標對齊 | 保留客戶 split，新增一組歷史統計特徵 |
| `m5` | [M5](https://www.kaggle.com/competitions/m5-forecasting-accuracy) | 預測窗口、遞迴推論與階層指標 | 在相同窗口與訓練成本下比較直接／遞迴預測 |

五個情境關聯真實比賽、已記錄閱讀的作者資料和方法卡，用於研究與協作回歸檢查。它們是**歷史解法研究情境**，本專案未重現冠軍訓練方案，也未產生新的官方分數。

```powershell
python skills/kaggle-solutions-skills/scripts/research_team.py scenarios --json
```

<a id="coverage"></a>

## 📚 知識涵蓋範圍

**v0.1.0 · 2026-10-04 匯入快照**。檔案與方法卡徽章及下表均為本版本的固定統計；更新後的即時數量以 `stats` 輸出為準。

| 檔案索引 | 已閱讀資料 | 已審查知識 |
| :--- | :--- | :--- |
| **717** 場比賽 | **13** 篇解法正文 | **21** 張方法卡 |
| **4,724** 筆解法連結紀錄 | **1** 份作者程式碼 README（Santa 2024） | 作者報告與待驗證的遷移假設 |
| **4,708** 個不同 URL | **7** 份 Skill 設計參考檔案，來自 **6** 個 GitHub 專案 | 適用條件、失敗風險與來源關聯 |

部分已閱讀的正文只提供局部方法或指向程式碼；125 場比賽尚無解法連結。上述數量表示檔案與研究涵蓋範圍，4,708 個 URL 的可存取性、正文閱讀和重現狀態仍需逐一確認。本專案尚未執行這些冠軍訓練方案。

<details>
<summary><strong>查看快照來源與可追溯紀錄</strong></summary>

上游儲存庫：[faridrashidi/kaggle-solutions](https://github.com/faridrashidi/kaggle-solutions)。

固定上游版本：[`6414951ae88d252a6c92d4489ba389b2b7cb40c7`](https://github.com/faridrashidi/kaggle-solutions/commit/6414951ae88d252a6c92d4489ba389b2b7cb40c7)。

- [本版本驗證紀錄](docs/validation.md)
- [知識欄位與證據狀態](skills/kaggle-solutions-skills/references/knowledge-schema.md)
- [來源與第三方授權](THIRD_PARTY_NOTICES.md)

</details>

## 📥 讀取解法正文

可選擇現有瀏覽器、MCP、官方 CLI，或安裝本專案的選用讀取相依套件：

```powershell
python -m pip install -e ".[kaggle-read]"
python skills/kaggle-solutions-skills/scripts/fetch_source.py https://www.kaggle.com/competitions/birdclef-2024/discussion/512197 --cache cache/sources
```

讀取工具使用現有 API token，不會印出或寫入憑證。Modern writeup 和舊論壇正文分別處理，並驗證取得的是原始貼文。它不提交、不上傳、不啟動雲端 notebook。Kaggle 內部讀取介面可能變更；存取失敗會留下明確狀態，應改用其他讀取方式。

<a id="maintenance"></a>

## 🌱 持續更新與知識審查

專案追蹤上游解法檔案的變更，經審查後更新索引，並結合作者資料與實際實驗證據完善方法卡。專案版本與上游快照分別記錄，更新會保留已有方法卡，不會自動覆寫已安裝的 Skill。

查看 [版本紀錄](CHANGELOG.md) 和 [Releases](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases) 取得更新；已有安裝可在安裝指令後加上 `--force` 更新。具體維護機制、排程與設定詳見 [維護文件](docs/daily-maintenance.md)。

### 專案結構

```text
kaggle-solutions-skills/
├── skills/kaggle-solutions-skills/   # 可安裝與分發的 Skill
│   ├── SKILL.md                     # Agent 入口與研究流程
│   ├── references/                  # 知識、來源與維護約定
│   └── scripts/                     # 檢索、校驗與正文讀取
├── docs/                           # 範例、路線與驗證紀錄
├── integrations/deepseek-harness/   # 原生外掛、bundle 與雙語資源
├── config/daily-agent-prompt.md     # 已授權的每日專案維護說明
├── scripts/project.py              # 專案檢查、安裝與封裝
├── tests/                          # 指令碼行為檢查
└── .github/workflows/               # CI 與上游更新檢查
```

## 🤝 參與維護

歡迎補充可追溯的解法資料、方法適用條件、失敗案例與實際實驗結果。提交前請閱讀 [貢獻約定](CONTRIBUTING.md) 和 [維護流程](skills/kaggle-solutions-skills/references/maintenance.md)。

| 開始貢獻 | 了解方向 | 查看演進 |
| :--- | :--- | :--- |
| [CONTRIBUTING](CONTRIBUTING.md) | [Roadmap](docs/roadmap.md) | [Changelog](CHANGELOG.md) |

---

<p align="center">
  基於 <a href="https://github.com/faridrashidi/kaggle-solutions">Farid Rashidi 的 Kaggle 解法檔案</a>，感謝解法作者的公開分享。<br>
  核心程式碼與新撰寫的指令採用 <a href="LICENSE">MIT</a>；上游檔案保留原 MIT 授權，連結內容遵循各自授權。<br>
  <sub>獨立維護的社群專案 · 非 Kaggle 官方專案</sub>
</p>
