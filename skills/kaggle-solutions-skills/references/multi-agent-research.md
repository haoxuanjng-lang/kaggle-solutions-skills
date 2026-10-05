# Multi-agent competition research

Generate bounded task packets for a real, indexed competition. Planning is an
offline operation; agents run only when the user asks for team research and the
chosen agent host dispatches the packets. No API account is required to plan.

```text
python <skill-dir>/scripts/research_team.py scenarios
python <skill-dir>/scripts/research_team.py plan --scenario otto --output workspaces/otto-research
python <skill-dir>/scripts/research_team.py validate workspaces/otto-research
```

Use an empty output directory outside the skill installation and Git history.
The command writes `plan.json`, five `tasks/<role>.json` packets, an empty
`outputs/` directory and a workspace README. It never starts model calls,
downloads competition data or executes author code. Five roles are a useful
default for these scenarios; the host can execute them serially when parallel
agents are unavailable.

## Roles and dependency graph

| Role | Input/output responsibility | Predecessors |
|---|---|---|
| scout | Competition profile, intended prediction units, known and unknown constraints | none |
| evidence | Original-author observations, locators and narrow source coverage | scout |
| validation | Split boundaries, leakage, metric and prediction-ID audit | scout |
| transfer | Conditional experiment proposals, controls and failure cases | evidence, validation |
| reviewer | Reconciled research brief, unresolved disagreement and experiment priorities | all four |

1. Dispatch scout with its `prompt`, `context` and `result_contract`.
2. Check that scout's JSON output is complete. Dispatch evidence and validation
   concurrently, giving both the scout output and their own packets.
3. When both outputs complete, dispatch transfer with their results.
4. Dispatch reviewer with every predecessor result. The host validates completed
   outputs and writes `research-brief.md` from the reviewed findings.

Each role owns one output file. Do not let concurrently running roles edit the
shared knowledge ledger, another role's file or the repository. Communicate
findings through structured outputs; upstream maintenance remains a separate
reviewed operation. For Codex collaboration tools, send each task's prompt plus
its JSON context to the delegated agent and ask it to write the task's specified
output in the current research workspace. Preserve dependencies when following
up with the same agent. Packet generation alone is `not_dispatched`.

## Evidence and bounded context

Every scenario links to an existing original-author source ledger and the exact
competition slug. Packets include at most six relevant cards and five archive
links. Cross-competition cards carry their other author ledgers too; do not
describe those other observations as experiments on the target competition.
Source hashes, read timestamps, reproduction status and card claim types travel
with the context. The original full article is not bundled.

`source_read` describes the recorded historical reading, not a fresh fetch by
the current agent. If the needed original passage is absent, fetch it through an
available research tool or record the limitation. An archive-only link stays
`linked_unread`. Metadata is pinned; a historical case does not establish that
the competition is currently running or that its rules are current. OTTO's
missing archive metric remains unknown until an official source is checked.

## Archive and author citations

Task context separates `archive_source` from the original-author ledgers in
`sources`. Archive identity includes the upstream commit and competition slug;
its URL points to the pinned upstream file. Use `archive_metadata` and that ID
for a profile fact, with a listed field locator such as `competition.metric`.
For OTTO, the archived metric is null: report that the archive does not supply
it, not that the official competition has no metric.

Use an author source ID and `author_report` for recorded author observations.
Use `maintainer_inference` for deductions, citing the archive or author source
that supports the reasoning. Archive sources cannot support `author_report` or
`locally_reproduced`; author sources cannot support `archive_metadata`. The
validator also rejects nonexistent archive field locators and altered provenance.
A valid citation does not establish that the statement is true or that an
archive link has been read. Current official status remains unknown.

Plans are checked against the installed skill's exact context and contract.
For pre-0.2.1 workspaces, keep the original skill version for validation, or
create a new empty workspace and have agents review and migrate findings.
Do not overwrite old results or relabel them as a new agent run.

## Result contract and merging

Use [team-task.json](../assets/templates/team-task.json) as the result template.
Replace placeholders, set the actual role and set `status` to `complete` only
after the role's research work finishes. Every finding has `statement`,
`claim_type`, `source_id` and a specific `locator`. Unknowns, experiment proposals
and disagreements are arrays; include a concise `handoff`.

```text
python <skill-dir>/scripts/research_team.py validate workspaces/otto-research --results
```

Validation checks all five outputs, field types, source identities and claim
types; it does not certify factual correctness. A `locally_reproduced` finding
requires a `run_record` pointing to measured evidence for subsequent inspection.
Official Kaggle scores additionally need the execution workflow's actual receipt.

When roles conflict, the reviewer records both claims, source IDs/locators, why
they differ and a proposed resolution experiment. Do not settle disagreement by
majority vote or a model's confidence. Keep unresolved items visible in the final
brief. Findings can be unknown; missing results must not be filled with invented
scores. Hand proposed experiments to the user's selected competition workflow,
which retains its existing training/submission authorization and requirements.

## Real research cases

The bundled registry contains OTTO recommendation, BirdCLEF 2024 audio, ROGII
geology, American Express customer-history prediction and M5 forecasting.
Their original author writeups have recorded reading provenance and reviewed
cards. All five cases are **historical research, not locally reproduced winning
solutions**. Add cases only when their indexed competition and original source
ledger resolve; preserve the evidence hierarchy in [knowledge-schema.md](knowledge-schema.md).
