# Knowledge structure and evidence

`assets/knowledge/` keeps independent layers:

| File | Meaning | Updated by |
|---|---|---|
| `competitions.yml` | Exact upstream file at the recorded commit | refresh |
| `competitions.jsonl` | Normalized competition metadata; solutions retain rank labels, original types and unread status | refresh |
| `manifest.json` | Upstream commit/time, file hashes, counts and inference labels | refresh |
| `last-refresh.json` | Added/removed/changed competition IDs and previous/current commit | refresh |
| `sources.json` | Read-source provenance and source role; no access tokens/full article text | source review |
| `patterns.json` | Paraphrased decisions, transfer conditions and tests | evidence review |
| `UPSTREAM-LICENSE.txt` | Archive copyright and license | refresh |

Schema version 1 is recorded in the manifest. Source records and cards use the following contract; tests/`validate` protect essential evidence relationships. Field additions can preserve version 1 if old readers still work; incompatible field changes need a migration and schema-version change.

## Source record

Required: `id`, `url`, `title`, `author`, `source_role`, `status`, `read_at`, `content_sha256`, `locator`, `retrieval_method`, `reproduction_status`. GitHub files additionally include `source_commit`. A solution source has its competition slug. Initial roles are `solution_writeup`, `author_code_readme` and `skill_reference`.

`status: source_read` means the pertinent body/code was retrieved and read; `content_sha256` hashes the retrieved text in UTF-8. The ledger proves traceability, not that the entire codebase was examined. State narrow coverage in `notes`. For unavailable or unread discoveries keep an appropriate status and do not cite them as read evidence.

## Pattern card

Required:

- `id`, `title`, `tags`, `competitions` for retrieval.
- `decision`: what changes in the next action.
- `applicability`: conditions that make transfer plausible.
- `pitfalls`: where the decision fails or the report is uncertain.
- `minimal_experiment`: a concrete candidate/control and observation.
- `evidence`: one or more references containing `source_id`, `locator`, `claim_type`, `observation`.
- `transfer_status` and `reviewed_at` for maintenance.

`claim_type` is `author_report`, `maintainer_inference` or `locally_reproduced`. Cards may mix these; do not upgrade an author's claim because code exists. `locally_reproduced` needs `run_record` pointing to an inspectable experiment ledger, with source/data/config/split identity and actual measurements. A scored Kaggle result additionally needs an official receipt/status record. Store private execution evidence in the user's competition workspace or private project, not in a distributable skill by accident.

If copying the [solution-card template](../assets/templates/solution-card.json), replace the placeholders and make the minimal experiment meaningful. Missing measurements remain null/unknown. Do not reconstruct absolute baseline scores by subtracting reported deltas from a final ensemble score.

## Important upstream irregularities

The archive root is a mapping containing `competitions`, not a bare list. Each competition's `solutions` can be null. `done` can be the string `"false"`; ordinary Python truthiness would interpret that incorrectly. `metric` can be `"-"` or empty. Ranks include nonnumeric labels such as `all solutions`. The same URL can appear more than once. The importer preserves each original link record and deduplicates only display results.

`kind` is an archive label such as code/description/kernel. A code label can point to a discussion. Different prize tracks can share a displayed archive rank. Do not use these fields as verified implementation type or official current ranking.

Refresh does not revise reviewed methods. If an upstream competition is removed, retain its reviewed source and resolve the card/archival relationship explicitly; validation should surface the mismatch for review.
