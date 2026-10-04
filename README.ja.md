<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Kaggle の解法を再利用できる知識へ：発見、読解、抽出、検証" width="100%">
</p>

<h1 align="center">kaggle-solutions-skills</h1>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <strong>日本語</strong> ·
  <a href="README.zh-TW.md">繁體中文</a>
</p>

<p align="center">
  <strong>過去の解法から着想を得て、確かな根拠を再利用できる Skill に蓄積する。</strong><br>
  オフライン知識ベース · DeepSeek Harness ネイティブプラグイン · 複数 Agent による調査 · 継続的な知識レビュー
</p>

<p align="center">
  <a href="https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/tag/v0.2.0"><img src="https://img.shields.io/badge/version-0.2.0-2563eb?style=flat-square" alt="バージョン 0.2.0"></a>
  <a href="#quick-start"><img src="https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&amp;logo=python&amp;logoColor=white" alt="Python 3.10 以降"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-10b981?style=flat-square" alt="MIT ライセンス"></a>
  <a href="https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/workflows/ci.yml"><img src="https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/workflows/ci.yml/badge.svg" alt="Skill の CI チェック"></a>
  <a href="#coverage"><img src="https://img.shields.io/badge/archive-717%20competitions-0ea5e9?style=flat-square" alt="スナップショット：717 コンペティション"></a>
  <a href="#coverage"><img src="https://img.shields.io/badge/reviewed-21%20method%20cards-8b5cf6?style=flat-square" alt="スナップショット：レビュー済み手法カード 21 件"></a>
  <a href="#deepseek"><img src="https://img.shields.io/badge/DeepSeek%20Harness-native%20plugin-6366f1?style=flat-square" alt="DeepSeek Harness ネイティブプラグイン"></a>
  <a href="#scenarios"><img src="https://img.shields.io/badge/research-5%20scenarios-0d9488?style=flat-square" alt="過去のコンペティションに基づく調査シナリオ 5 件"></a>
</p>

<p align="center">
  <a href="#quick-start">クイックスタート</a> ·
  <a href="#workflow">ワークフロー</a> ·
  <a href="#deepseek">DeepSeek プラグイン</a> ·
  <a href="#team">Agent 連携</a> ·
  <a href="#scenarios">コンペティションのシナリオ</a> ·
  <a href="#coverage">知識の収録範囲</a> ·
  <a href="docs/examples/rogii-research-brief.md">調査例</a> ·
  <a href="#maintenance">継続的な更新</a>
</p>

---

Kaggle の解法は、フォーラム、Notebook、作者のリポジトリに散在しています。優勝解法のリンクを見つけても、検証方法は信頼できるのか、どの判断が現在のデータに適しているのか、複数の Agent の調査をどう統合するのか、次のコンペティションで経験をどう再利用するのかを考える必要があります。

本プロジェクトは [faridrashidi/kaggle-solutions](https://github.com/faridrashidi/kaggle-solutions) を解法発見の索引として利用し、読んだ作者資料を出典と適用条件付きの手法カードに整理します。Codex と DeepSeek Harness は同じ知識ベースを利用し、**類似する解法、検証上のリスク、比較可能な最小実験**を提供します。

| 🔎 関連する解法を探す | 🧩 Agent と協力して調査する | 🌱 長期的な知識を蓄積する |
| :--- | :--- | :--- |
| キーワードやモダリティでコンペティションを検索。Codex Skill と Harness のネイティブツールが同じ知識ベースを利用します。 | 探索、根拠の確認、検証、応用、統合の 5 つの役割が出典と未確認事項を引き継ぎ、見解の相違も記録します。 | アーカイブと手法カードをレビューして更新。実際の実験と反例を記録し、再利用できる調査知識を改善します。 |

<a id="quick-start"></a>

## ⚡ クイックスタート

### 1. コマンド 1 つでインストール

**Node.js 20+** が必要です。公開 Release から Skill 一式をインストールでき、GitHub token は不要です。

```powershell
npx --yes --package=https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.2.0/haoxuanjng-lang-kaggle-solutions-skills-0.2.0.tgz kaggle-solutions-skills install
```

既存のインストールを更新する場合は `--force` を追加します。`--destination <skill-folder>` でインストール先を指定できます。

📦 [GitHub Packages](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/packages) · [npm インストールパッケージ](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.2.0/haoxuanjng-lang-kaggle-solutions-skills-0.2.0.tgz) · [Skill ZIP](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/download/v0.2.0/kaggle-solutions-skills-0.2.0.zip)

インストールと今後の配布方法の詳細：[Distribution](docs/distribution.md)。

<details>
<summary><strong>ソースからインストール / GitHub npm registry を利用する</strong></summary>

**Python 3.10+** が必要です。オフラインの `search` / `show` / `patterns` は標準ライブラリのみを使用します。開発用インストールには、更新と検証に必要な PyYAML が含まれます。

```powershell
git clone https://github.com/haoxuanjng-lang/kaggle-solutions-skills.git
cd kaggle-solutions-skills
python -m pip install -e .
python scripts/project.py install
```

GitHub Packages の npm パッケージは `@haoxuanjng-lang/kaggle-solutions-skills` で、`npm.pkg.github.com` に公開しています。[GitHub の公式ガイド](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry) に従って registry の認証を済ませた後、次のコマンドを実行します。

```powershell
npx --yes --registry=https://npm.pkg.github.com @haoxuanjng-lang/kaggle-solutions-skills@0.2.0 install
```

通常のダウンロードとインストールには、上記の Release コマンドをそのまま利用できます。registry の設定は不要です。Skill 内の調査ツールの実行には Python 3.10+ を使用し、Node.js はファイルのインストールを担当します。

</details>

インストール後、新しいチャットで呼び出します。

```text
$kaggle-solutions-skills このコンペティションに類似する問題と解法を探し、根拠のある実験方針をまとめてください。
```

### 2. 知識を検索

```powershell
# 現在のアーカイブと調査の収録範囲を確認
python skills/kaggle-solutions-skills/scripts/solutions.py stats

# 類似する問題を検索
python skills/kaggle-solutions-skills/scripts/solutions.py search "医学影像" --modality vision --limit 5

# 指定したコンペティションの解法の手がかりを確認
python skills/kaggle-solutions-skills/scripts/solutions.py show rogii-wellbore-geology-prediction --top-rank 5 --json

# 応用できる手法を検索
python skills/kaggle-solutions-skills/scripts/solutions.py patterns "蒸馏" --json
```

### 3. 調査から実験へ

| やりたいこと | 呼び出し例 |
| :--- | :--- |
| 過去の手法を比較する | `$kaggle-solutions-skills OTTO の優勝解法の候補検索とランキング戦略を比較し、最小の比較実験を提案してください。` |
| コンペティションの経験を蓄積する | `$kaggle-solutions-skills 今回の実験での成功と失敗を手法カードに整理し、実際の結果を保持してください。` |
| 知識ベースを更新する | `$kaggle-solutions-skills 解法の索引を更新し、上流の変更をレビューして、インストール済みのバージョンを確認してください。` |

📖 [Skill のエントリーポイント](skills/kaggle-solutions-skills/SKILL.md) · [ROGII の調査引き継ぎ例](docs/examples/rogii-research-brief.md)

<details>
<summary><strong>インストール先と ZIP 配布</strong></summary>

デフォルトのインストール先は `$CODEX_HOME/skills/kaggle-solutions-skills` です。未設定の場合は `~/.codex/skills/kaggle-solutions-skills` になります。`python scripts/project.py install --destination <skill-folder>` で変更できます。

インストールでは Skill とオフライン知識のみをコピーします。キャッシュ、上流リポジトリの checkout、個人のコンペティションファイルは元のプロジェクトに残ります。

```powershell
python scripts/project.py package
```

出力する ZIP には Skill、オフライン知識、MIT ライセンス、上流のライセンスが含まれ、CRC とファイルのバイト列を検証します。公開済みのバージョンは [Releases](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases) からも取得できます。

</details>

<a id="workflow"></a>

## 🧭 ワークフロー

![コンペティションの課題から手法カード、実験の引き継ぎ、知識へのフィードバックまで](docs/assets/research-workflow.svg)

| 段階 | 成果物 | 保持する根拠 |
| :--- | :--- | :--- |
| **検索** | 類似するコンペティションと解法候補 | コンペティション、リンク、順位の手がかり、上流のバージョン |
| **読解** | 原文とコードの根拠 | 作者の記述、コードの位置、アクセス状況 |
| **抽出** | 条件付きの手法カード | 適用前提、失敗条件、出典との関連 |
| **引き継ぎ** | 最小の比較実験 | 対象の仮説、検証方法、リソースの制約 |
| **フィードバック** | 新たな根拠と反例 | 実際の結果、実行環境、バージョン |

実際の学習、実行、Kaggle 公式スコアの取得は、ユーザーが選んだコンペティション用 workflow に調査結果を引き継いで行います。`agentic-kaggle-skill` を使用している場合は、その手順に従います。

> **根拠の区別**：アーカイブのリンク、作者の報告、応用の仮説、ローカル実験、公式スコアは、それぞれ分けて記録します。過去の順位は解法発見の手がかりになりますが、対象コンペティションでの効果には実際の検証が必要です。

<a id="deepseek"></a>

## 🐋 DeepSeek Harness ネイティブプラグイン

### 現在の課題とプラグインでできること

| 現在の課題 | Harness 内での解決方法 | 成果物 |
| :--- | :--- | :--- |
| 多くの手法が見つかっても、現在の問題に似ているか判断しづらい | 問題、モダリティ、過去のコンペティションで検索し、対応する解法の手がかりを確認 | 類似するコンペティション、作者の出典、要確認事項 |
| 優勝解法の工夫を応用する際に、検証方法やデータの境界を見落としやすい | 条件付きの手法カードを検索し、根拠を確認する Agent と検証を担当する Agent が別々に調査 | 適用条件、リークのリスク、失敗条件、最小の比較実験 |
| 複数の Agent が同じ検索を繰り返し、文脈が失われ、統合時に作者の報告と実際の実験が混同される | 独立したタスクパケット、依存関係のグラフ、出典の文脈を生成し、reviewer が統合 | 引き継ぎ可能な調査結果、未解決の見解の相違、実験の提案 |

Harness に、新しいコンペティションに類似する問題の検索、特定のコンペティションの解法比較、調査チームの編成、実際の実験結果の知識化を依頼できます。オフライン検索とタスク生成はすぐに利用できます。新たなモデル分析には Harness の設定を使用し、実験と公式成績はコンペティション実行用 workflow で取得します。

同じ npm パッケージに Cordis プラグイン、bundle patch、2 言語のメタデータ、ツールのアイコンを収録しています。ローカルの **Harness `0.1.0-rc.6` の完全な Web host** で 6 つのツールの呼び出しに成功し、プラグイン管理画面でマウント済み・有効と表示されることを確認しました。公式の **`0.2.0-rc.2` ツールランタイム** でも、登録、呼び出し、エラーの伝播、アンロードを検証しています。[ローカル検証記録とスクリーンショット](docs/harness-local-validation.md) を参照してください。

[Release](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases/tag/v0.2.0) から `.tgz` をダウンロードし、ファイルのあるディレクトリで実行します。

```bash
npx @deepseek-ai/dsh@0.2.0-rc.2 plugin --profile kaggle add ./haoxuanjng-lang-kaggle-solutions-skills-0.2.0.tgz
npx @deepseek-ai/dsh@0.2.0-rc.2 --profile kaggle --dump-config
```

| 検索ツール | 根拠の確認ツール | 連携ツール |
| :--- | :--- | :--- |
| `kaggle_solutions_search` | `kaggle_solutions_show` | `kaggle_research_scenarios` |
| `kaggle_solutions_stats` | `kaggle_solutions_patterns` | `kaggle_research_plan` |

オフラインツールには追加の API key は不要です。モデルとの対話には Harness 自体の設定を使用します。プラグインはタスクパケットを生成し、実際の割り当てにはホストの subagent/workflow 機能を使用します。公式 Harness は現在 developer preview です。互換性の範囲と workspace の設定は [プラグインガイド](docs/deepseek-harness.md) を参照してください。

コミュニティでの公開：[1024Store](https://deepseek1024.com/plugins/haoxuanjng-lang/kaggle-solutions-skills) に掲載済みです（[登録 PR はマージ済み](https://github.com/imsai-sh/awesome-deepseek-harness-plugins/pull/567)）。コミュニティのディレクトリへの掲載であり、DeepSeek 公式の認証ではありません。インストールには上記の検証済み Release パッケージを使用してください。

<a id="team"></a>

## 🤖 複数 Agent による協調調査

![5 つの役割を持つ調査チームの依存関係と根拠の引き継ぎ](docs/assets/agent-team.svg)

```powershell
python skills/kaggle-solutions-skills/scripts/research_team.py plan --scenario otto --output workspaces/otto-research
python skills/kaggle-solutions-skills/scripts/research_team.py validate workspaces/otto-research
```

各役割には独立したタスク、固定された出典の文脈、結果の契約、前提となる結果のパスを渡します。根拠の読解と検証レビューは並行して実行できます。応用分析は両方の完了を待ち、最後に reviewer が追跡可能な知見、見解の相違、最小実験をまとめます。

Codex では次のように依頼できます。

```text
$kaggle-solutions-skills 複数の Agent で OTTO の候補検索とランキングの手法を分析し、検証でのリークをレビューして、最小の応用実験を提案してください。対象の評価指標が不明な場合は未確認のままにしてください。
```

**タスクパケットの生成 ≠ Agent の実行完了。** ホストで実際に実行した後、`validate <研究目录> --results` で各役割の結果と出典との関連を確認します。形式のチェックに通っても、事実が出典に裏付けられているかは調査者が判断する必要があります。[連携フロー](skills/kaggle-solutions-skills/references/multi-agent-research.md) · [実際の調査での使い方](docs/examples/team-research.md)

[OTTO の実際の調査試用](docs/examples/otto-team-run.md) を 1 回完了しています。5 つの役割が依存関係に沿って調査し、そのうち evidence / validation は独立した Agent が並行して実行しました。キャッシュした作者の本文を読んで、応用実験の調査レポートを作成しました。この記録は調査フローの検証であり、コンペティションでの効果はまだ検証していません。

<a id="scenarios"></a>

## 🏁 実際のコンペティションに基づく調査シナリオ

| シナリオ ID | 元のコンペティション | 調査の重点 | 最小実験の方向性 |
| :--- | :--- | :--- | :--- |
| `otto` | [OTTO](https://www.kaggle.com/competitions/otto-recommender-system) | Session の境界、候補検索とランキング | 候補生成を固定し、ランキング段階だけを比較 |
| `birdclef-2024` | [BirdCLEF 2024](https://www.kaggle.com/competitions/birdclef-2024) | 音声の文脈、出典の品質、疑似ラベルの分離 | 同じ split と予算で、文脈または疑似ラベルの方針を 1 つ変更 |
| `rogii` | [ROGII](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction) | 井戸をまたぐ検証、位置合わせ、信頼性に基づくルーティング | ベースラインを固定し、位置合わせまたはルーティングの単一の変更を比較 |
| `amex` | [American Express](https://www.kaggle.com/competitions/amex-default-prediction) | 顧客の分離、履歴特徴量、評価指標との整合 | 顧客単位の split を維持し、履歴の統計特徴量を 1 組追加 |
| `m5` | [M5](https://www.kaggle.com/competitions/m5-forecasting-accuracy) | 予測期間、再帰的推論、階層的な評価指標 | 同じ期間と学習コストで、直接予測と再帰予測を比較 |

5 つのシナリオは、実際のコンペティション、読んだことを記録済みの作者資料、手法カードを関連付け、調査と連携の回帰チェックに使用します。これらは**過去の解法を調査するシナリオ**です。本プロジェクトで優勝解法の学習手順を再現したり、新たな公式スコアを取得したりしたものではありません。

```powershell
python skills/kaggle-solutions-skills/scripts/research_team.py scenarios --json
```

<a id="coverage"></a>

## 📚 知識の収録範囲

**v0.1.0 · 2026-10-04 に取り込んだスナップショット**。アーカイブと手法カードのバッジ、および下表は、このバージョンの固定された統計です。更新後の最新件数は `stats` の出力で確認してください。

| アーカイブの索引 | 読んだ資料 | レビュー済みの知識 |
| :--- | :--- | :--- |
| **717** コンペティション | 解法の本文 **13** 件 | 手法カード **21** 件 |
| 解法リンクの記録 **4,724** 件 | 作者のコード README **1** 件（Santa 2024） | 作者の報告と、検証が必要な応用の仮説 |
| 異なる URL **4,708** 件 | **6** つの GitHub プロジェクトから Skill 設計の参考ファイル **7** 件 | 適用条件、失敗のリスク、出典との関連 |

読んだ本文の一部は、手法の一部分のみを説明しているか、コードへのリンクを示しています。125 コンペティションには解法リンクがありません。上記の件数はアーカイブと調査の収録範囲を表します。4,708 件の URL について、アクセス可能性、本文の読解、再現状況は個別に確認する必要があります。本プロジェクトは、これらの優勝解法の学習手順をまだ実行していません。

<details>
<summary><strong>スナップショットの出典と追跡可能な記録</strong></summary>

上流リポジトリ：[faridrashidi/kaggle-solutions](https://github.com/faridrashidi/kaggle-solutions)。

固定した上流のバージョン：[`6414951ae88d252a6c92d4489ba389b2b7cb40c7`](https://github.com/faridrashidi/kaggle-solutions/commit/6414951ae88d252a6c92d4489ba389b2b7cb40c7)。

- [このバージョンの検証記録](docs/validation.md)
- [知識のフィールドと根拠の状態](skills/kaggle-solutions-skills/references/knowledge-schema.md)
- [出典とサードパーティのライセンス](THIRD_PARTY_NOTICES.md)

</details>

## 📥 解法の本文を読む

既存のブラウザ、MCP、公式 CLI を選ぶか、本プロジェクトの任意の読み取り依存関係をインストールできます。

```powershell
python -m pip install -e ".[kaggle-read]"
python skills/kaggle-solutions-skills/scripts/fetch_source.py https://www.kaggle.com/competitions/birdclef-2024/discussion/512197 --cache cache/sources
```

読み取りツールは既存の API token を使用し、認証情報を表示したり書き出したりしません。Modern writeup と旧フォーラムの本文をそれぞれ処理し、取得した内容が元の投稿であることを確認します。提出、アップロード、クラウド Notebook の起動は行いません。Kaggle 内部の読み取りインターフェースは変わる可能性があります。アクセスに失敗した場合は明確な状態を記録し、別の読み取り方法に切り替えます。

<a id="maintenance"></a>

## 🌱 継続的な更新と知識レビュー

プロジェクトは上流の解法アーカイブの変更を追跡し、レビュー後に索引を更新します。作者資料と実際の実験の根拠を組み合わせて手法カードを改善します。プロジェクトのバージョンと上流のスナップショットは別々に記録します。更新時には既存の手法カードを保持し、インストール済みの Skill を自動で上書きすることはありません。

更新内容は [変更履歴](CHANGELOG.md) と [Releases](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/releases) で確認できます。既存のインストールを更新するには、インストールコマンドに `--force` を追加してください。具体的なメンテナンスの仕組み、スケジュール、設定は [メンテナンス文書](docs/daily-maintenance.md) にまとめています。

### プロジェクトの構成

```text
kaggle-solutions-skills/
├── skills/kaggle-solutions-skills/   # インストール・配布用の Skill
│   ├── SKILL.md                     # Agent の入口と調査フロー
│   ├── references/                  # 知識、出典、保守の取り決め
│   └── scripts/                     # 検索、検証、本文の読み取り
├── docs/                           # 例、ロードマップ、検証記録
├── integrations/deepseek-harness/   # ネイティブプラグイン、bundle、2 言語のリソース
├── config/daily-agent-prompt.md     # 許可された毎日のプロジェクト保守指示
├── scripts/project.py              # プロジェクトのチェック、インストール、パッケージ化
├── tests/                          # スクリプトの動作チェック
└── .github/workflows/               # CI と上流の更新チェック
```

## 🤝 メンテナンスへの参加

追跡可能な解法資料、手法の適用条件、失敗例、実際の実験結果の追加を歓迎します。提出前に [コントリビューションの取り決め](CONTRIBUTING.md) と [メンテナンスフロー](skills/kaggle-solutions-skills/references/maintenance.md) をお読みください。

| 貢献を始める | 今後の方向性 | 変更を確認する |
| :--- | :--- | :--- |
| [CONTRIBUTING](CONTRIBUTING.md) | [Roadmap](docs/roadmap.md) | [Changelog](CHANGELOG.md) |

---

<p align="center">
  <a href="https://github.com/faridrashidi/kaggle-solutions">Farid Rashidi の Kaggle 解法アーカイブ</a>を基にしています。解法を公開してくださった作者の皆様に感謝します。<br>
  コアコードと新規の指示は <a href="LICENSE">MIT</a> ライセンスです。上流アーカイブは元の MIT ライセンスを保持し、リンク先の内容は各々のライセンスに従います。<br>
  <sub>独立して維持されるコミュニティプロジェクト · Kaggle の公式プロジェクトではありません</sub>
</p>
