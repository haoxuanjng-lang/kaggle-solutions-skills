# v0.1.0 verification record

Date: 2026-10-04, Asia/Shanghai. Code/skill baseline:
`57d38b57444eba3ba003349e90474b6125d7ff2e`.

| Check | Observed result |
|---|---|
| Local behavior tests | 21 passed |
| Skill Creator `quick_validate.py` | Source and installed entrypoint valid |
| Knowledge consistency | 717 competitions, 4,724 link records, 21 cards, 21 read-source records; hashes and evidence relationships valid |
| Optional Kaggle read adapter | Modern `/c/.../writeups/...` and legacy original-message retrieval succeeded; author-body hashes matched the maintained source ledger |
| Live upstream refresh | Retrieved the pinned upstream commit; fresh normalized index validated |
| GitHub anonymous rate limit | Observed HTTP 403; authenticated `gh` fallback succeeded without exporting credentials |
| Installed skill | 18 files, 2,479,342 bytes; every copied file byte-verified; independent query and knowledge validation succeeded |
| ZIP | 18 allowlisted files, 345,849 bytes; CRC and source-byte comparison passed |
| Cross-platform CI | [All four jobs passed](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37186016086): Windows/Ubuntu, Python 3.11/3.13 |
| Weekly updater | [Manual no-update run passed](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37186076796), reporting `changed: false` at the current upstream commit |

The workflow dependencies were subsequently moved to the live official
checkout v7.0.1/setup-python v7.0.0 commits after runner logs exposed deprecated
Node 20 actions. Their new CI results are available from repository Actions.

No local reproduction of the archived winning model/agent pipelines was
attempted. No competition submission, data upload or cloud training run was made.
Structural checks and retrieval tests establish tool behavior in these scenarios,
not method-card gains on a new competition. The updater's new-commit PR branch
is configured but was not triggered against a real new upstream commit during
this verification; the no-change path was exercised live.

Raw research/source caches remain local and excluded from Git and the skill ZIP.
The source/installed metadata and hashes should be checked again after future
updates; these measurements describe this release.
