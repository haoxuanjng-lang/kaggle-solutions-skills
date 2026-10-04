# Maintaining the skill

Use this when the user asks to update the archive, incorporate new evidence or release an installed version. A refresh downloads small metadata files only; it does not run competition code or collect all solution bodies.

## Archive refresh

```text
python <skill-dir>/scripts/solutions.py refresh
python <skill-dir>/scripts/solutions.py validate
```

For reproducible import from an existing source checkout:

```text
python <skill-dir>/scripts/solutions.py refresh --source-dir <path-to-kaggle-solutions-checkout>
```

The importer reads the exact committed YAML via `git show HEAD:data/competitions.yml`, so dirty checkout content cannot be mislabeled as that commit. Network refresh resolves `main` or `--ref` first, then reads YAML/license at the resolved immutable commit. It stages output, writes the manifest last and retains curated files. Validate before trusting a new snapshot; a interrupted refresh can leave inconsistent files and checksums expose that condition.

Inspect `last-refresh.json`: changes include metadata and link additions/removals. Same-commit refresh has no content differences. An upstream refresh time does not make old post links currently verified. The new upstream commit is not automatically a new method-card version.

Network refresh uses `GH_TOKEN` / `GITHUB_TOKEN` for the GitHub API when present. On anonymous API 403/429 it can reuse an existing authenticated `gh` session without exporting the stored token. If neither path works, use the checkout importer or wait for the API quota to reset; the existing snapshot remains intact.

## Evidence additions

Read relevant new sources and record their identity/hash/locator, then add or amend cards under the schema. Add counterexamples rather than erasing inconvenient failures. Check whether a new report merely repeats an existing method or materially changes an applicability condition. Avoid verbatim article redistribution; retain original URLs and original paraphrases. Credit author code and review its own license before reuse.

When a method is contradicted, narrow its conditions or retain competing observations with context. If a source disappears, keep historical provenance and mark the latest access attempt separately. Do not delete an already-reviewed card just because a link temporarily fails.

## Project-level release

From the maintained project root, run:

```text
python -m pip install -e .
python -m unittest discover -s tests -v
python skills/kaggle-solutions-skills/scripts/solutions.py validate
python scripts/project.py check
python scripts/project.py install
python scripts/project.py package
```

The install helper copies only the skill folder into the normal Codex skills directory and preserves no private caches or upstream checkout. It rejects an unrelated existing destination. Maintain the project as the source of truth; edits made solely to an installed copy are not project history.

Update `VERSION`, `pyproject.toml`, skill frontmatter `metadata.version` and changelog for reviewed behavior/card changes; project checks require the versions to agree. An archive-only refresh can retain the skill version because provenance has its own commit identity. Do not claim benchmark gains from structural validation or unit tests.

## GitHub maintenance

The project includes CI for pull requests/pushes and a weekly upstream-sync workflow. Scheduled sync checks for new upstream commits, refreshes/validates/tests, then creates a review PR when content changes. It does not automatically merge or change the installed skill. Failed checks remain visible in Actions.

The workflow needs repository Actions permissions allowing its token to create pull requests. If that setting is unavailable, the scheduled job still reports the failure; run the same refresh locally and submit a normal PR. A private repository's Actions quotas/settings apply. This workflow only maintains the archive; research and method-card additions remain evidence-reviewed work.

See the project roadmap for next improvements. Do not turn a future milestone into an extra prerequisite for today's ordinary research.
