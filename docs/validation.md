# Verification records

## v0.2.2 — Stable source hashes across platforms

Date: 2026-10-07, Asia/Shanghai.

- A regression scenario returned text containing CRLF and bare CR. The fetch
  helper preserved those exact UTF-8 cache bytes, recorded their matching
  `cached_bytes_sha256`, and produced the same normalized `content_sha256` as
  the equivalent LF text. This is adapter-returned text, not an HTTP-byte hash.
- All 33 Python tests passed, including the new fetch/cache regression. npm
  tests passed, and all six plugin tests passed with the pinned official
  `dsh-tools@0.2.0-rc.2`, `dsh-system-prompt@0.2.0-rc.2`, and
  `cordis@4.0.4` runtime packages.
- The local daily maintenance suite passed all 15 deterministic checks,
  including plan generation and validation for all five historical scenarios.
  No model call, competition training, or Kaggle submission was performed.
- Official Harness `0.2.0-rc.2` was tied to its source-tag commit `639ed01`.
  Current master / `0.2.1-alpha.1` at `5badb15` was source-reviewed, but its
  registration/execution path was not completed and is not claimed compatible.
- The existing archive refresh [PR #2](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/pull/2)
  was unblocked, passed all six Windows/Ubuntu checks, and merged separately.
  It added four archive competitions without changing curated cards or source
  records; those new links remain archive metadata, not read evidence.

Public distribution follow-up: 2026-10-09, Asia/Shanghai.

- [Publication succeeded](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37644451296)
  from `b6436b50d510395d35f70ba5225ca7474aa24faf`. GitHub's package API
  confirmed public visibility; all three Release assets were uploaded.
- Anonymous HTTP downloads of the existing TGZ (374,032 bytes) and ZIP
  (352,975 bytes) matched the published `SHA256SUMS.txt`. TGZ SHA256:
  `0acad9888bd096d1400d98b61a8a1badde98b4a67c496cf02afdf75523778b95`;
  ZIP SHA256:
  `ecab4c6f52b8fd61a4fbc02091e689d256f8a8d4ff3d9c15a2979d67ce7e6711`.
- Public Release URL `npx` installation into a fresh destination succeeded.
  All 22 installed files matched the maintained skill byte-for-byte. Installed
  `stats` reported 721 competitions, 4,768 links, 21 cards and 21 source records;
  installed OTTO plan generation and validation succeeded (`not_dispatched`,
  `results_checked: false`). No research-agent execution is implied.
- The local maintenance suite passed all 15 checks, including 33 Python tests
  and all five scenario plans/validators. A separate npm run with the pinned
  official runtime passed all 10 tests without skips. Knowledge validation
  passed. These checks do not establish newer Harness compatibility.
- Latest observed cloud [daily maintenance](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37741600772)
  and [archive review](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37741841795)
  succeeded on October 8; archive review reported no change at
  `dc9a449d84841cb9d03c110a4db16192c243d907`. An October 9 run had not
  appeared when inspected; it is not recorded as passed.

This follow-up corrects stale installation commands in the distribution guide
and records observed evidence. It does not rebuild or replace v0.2.2 assets.

## v0.2.1 — Separate archive and author citation identities

Date: 2026-10-05, Asia/Shanghai.

- Local daily maintenance passed all 15 checks: project integrity, 32 Python
  tests, npm tests with the pinned official runtime enabled, npm pack preview,
  scenario discovery, and plan/validation smoke checks for all five scenarios.
- `solutions.py validate` passed: 717 competitions, 4,724 links, 21 cards and
  21 source records. Curated knowledge and the upstream snapshot were unchanged.
- Regression checks accept OTTO's null archive metric with its archive identity
  and reject author/reproduction misattribution, invalid field locators, and
  modified archive provenance.
- An independent agent completed a real OTTO trial from the updated skill and
  task packets, executing all five roles serially in dependency order. All five
  outputs and its brief passed `validate --results`; independent diff review
  found no blocking defects. It cited the archived title/year/null metric with
  the archive ID, recorded candidate retrieval/reranking under author source
  `otto`, and preserved untested transfer hypotheses. This was one agent in five
  roles, not five independent researchers or fresh original-source reading.
- Official Harness master still resolved to `5badb15009ae1756c3afe0ae0cef1faafc290ccc`;
  the official tool-authoring reference was read again. Compatibility remains
  pinned to `dsh-tools@0.2.0-rc.2` and `cordis@4.0.4`. No new full Web-host run
  or API-key conversation was attempted.
- Existing cloud [daily maintenance](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37273539658)
  and [archive sync](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37273862052)
  passed. Sync reported no upstream change at `6414951ae88d252a6c92d4489ba389b2b7cb40c7`.

These checks establish research-tool behavior, not model gains or official
Kaggle scores. Old workspaces require their original skill version or reviewed
migration into a new workspace; generated plans are never evidence of dispatch.

## v0.2.0 — Native Harness plugin and daily research maintenance

Date: 2026-10-04, Asia/Shanghai. Publication follows local full-host validation.

| Check | Observed result |
|---|---|
| Local behavior | 31 Python tests passed; 10 npm tests passed with the official runtime installed; project and knowledge consistency checks passed |
| Portable skill | Skill Creator entrypoint validation passed; 22 allowlisted files |
| Actual local Harness | Installed unpublished tarball into a dedicated profile of the existing `dsh@0.1.0-rc.6`; full Web host started; all six host tool executions succeeded; plugin UI showed mounted and enabled |
| Official new runtime | `dsh-tools@0.2.0-rc.2` / `cordis@4.0.4`: registration, execution, errors and disposal passed |
| Independent research use | [OTTO role workflow](examples/otto-team-run.md) completed, including two independent parallel evidence/validation agents; clarified result contract rejected malformed results |
| Daily deterministic checks | Actual local maintenance report passed all 15 checks, including planning and validating all five historical scenarios |
| Local daily AI maintenance | Windows task registered for 09:00 Asia/Shanghai; first scheduled execution is 2026-10-05; read-only live Codex smoke passed |
| Cross-platform CI | [All six jobs passed](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37211953083), including official-runtime tests on Windows and Ubuntu |
| Cloud daily maintenance | [Manual run passed](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37211968245); five scenario plans and validators succeeded |
| Cloud upstream review | [Manual run passed](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37211973547); upstream unchanged, no PR created |
| Public publication | [Publishing succeeded](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37212052475); GitHub Packages version `0.2.0` confirmed public |
| Release assets | npm tarball 361,090 bytes; portable ZIP 356,100 bytes; checksums attached; all assets uploaded |
| Public installation | Public Release URL `npx` installed 22 files into a fresh directory; installed `stats`, OTTO plan generation and validation succeeded |
| Community directory | [1024Store catalog PR merged](https://github.com/imsai-sh/awesome-deepseek-harness-plugins/pull/567), static/merge/sync checks passed, and [live listing](https://deepseek1024.com/plugins/haoxuanjng-lang/kaggle-solutions-skills) was visible in the browser; this is community discovery, not official certification |

Release source: `e2978db4d3148e0e8ffe1f92a0c530a2783d4f54`.
Published npm tarball SHA256:
`08bf118ff3ec14c126547913cd4ebc8155fe9ff3c9c64d954000e681c1c22323`.
Portable ZIP SHA256:
`58c028bd1d3d7ad6d6f71d3e9721aa87fbb2fe0048951eaf0daf3534335383c1`.
Later documentation changes do not replace these immutable published packages.

The Harness test used an isolated empty credential file to avoid an existing
old-host credential-format incompatibility. Existing credentials and profiles
were preserved. No API-key model conversation, competition training or scored
submission was tested. The old UI displays the module name rather than the
exported localized metadata. See [full host evidence](harness-local-validation.md).

## v0.1.1 — Public distribution and README

Date: 2026-10-04, Asia/Shanghai. Package source commit:
`2fa26616357acaeaa58b4eca0cce62f971d3d519`; publishing workflow fix:
`4146220d5137b6b1cb2ff7600e70f293a9b29f7e` (no distributed-file changes).

| Check | Observed result |
|---|---|
| Repository visibility | GitHub API reports `PUBLIC`; logged-out browser can load the repository |
| README rendering | All 8 images/badges loaded on GitHub; all 4 custom navigation anchors have targets; banner and workflow screenshots visually checked |
| Local validation | Project/knowledge checks, 21 Python tests and 4 npm installer tests passed |
| Cross-platform CI | [All 6 jobs passed](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37187600183): 4 Python jobs and npm installer tests on Windows/Ubuntu |
| npm publication | [Publish workflow succeeded](https://github.com/haoxuanjng-lang/kaggle-solutions-skills/actions/runs/37187600956); GitHub API reports package visibility `public` |
| Built-package installation | Workflow installed the actual `.tgz` and queried its knowledge; local public-URL `npx` installation also succeeded, copying 18 skill files |
| Release assets | `.tgz` (346,368 bytes), ZIP (345,807 bytes), `SHA256SUMS.txt`; GitHub reports all assets `uploaded` |
| Public npm tarball digest | SHA256 `cc671c28c7624a2a6b3ff396dee45c395f0df6467843bdaafad21e9f9e7859b8` |
| Public ZIP digest | SHA256 `a0775f498e7ef514805b2433e69086a1d567bdb13553787a6dc3d3da710e4c34` |

The first publish attempt failed because npm interpreted an unprefixed local
tarball path as a GitHub repository shorthand. Explicit `./dist/...` paths and
an actual tarball installation step fixed the publishing workflow. The package
was then published successfully. GitHub npm registry installation needs
authentication; public Release downloads provide the credential-free path.

These checks verify distribution and research-tool behavior. The archived
solutions and method-card transfer hypotheses remain unvalidated by competition
training or official scored submissions in this project.

## v0.1.0 — Initial skill

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
