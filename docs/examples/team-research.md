# A research team for BirdCLEF 2024

This executable example retrieves a real competition from the bundled archive
and creates five role packets from its reviewed author evidence. It makes no
paid model calls and reports no reproduced score.

```powershell
python skills/kaggle-solutions-skills/scripts/research_team.py scenarios --json
python skills/kaggle-solutions-skills/scripts/research_team.py plan --scenario birdclef-2024 --output workspaces/birdclef-research
python skills/kaggle-solutions-skills/scripts/research_team.py validate workspaces/birdclef-research
```

The BirdCLEF case resolves to
[BirdCLEF 2024](https://www.kaggle.com/competitions/birdclef-2024) and the ledger
entry for chemrovkirill's
[1st-place author writeup](https://www.kaggle.com/competitions/birdclef-2024/discussion/512197).
The writeup was read when the source ledger was created; this command retrieves
that provenance and paraphrased cards, not the full original article. Its
reproduction status is `not_attempted`.

The role packets carry four reviewed decisions: pseudo-label fold isolation,
audio-context alignment, source-quality audit and inference budget. The scout
profiles context; evidence and validation work in parallel after scout; transfer
proposes one controlled change; reviewer reconciles the outputs.

Ask an agent host to execute the packets:

> Use the generated BirdCLEF plan for multi-agent research. Dispatch scout first,
> then evidence and validation concurrently. Give transfer both predecessor
> outputs and reviewer all outputs. Preserve source IDs, distinguish author
> reports from transfer hypotheses, and record unresolved disagreements. Write
> the completed role JSON files and a reviewed research brief into this workspace.

After execution:

```powershell
python skills/kaggle-solutions-skills/scripts/research_team.py validate workspaces/birdclef-research --results
```

A useful experiment proposal is a fixed supervised baseline versus one
context-window or pseudo-label change on an identical recording-separated split.
Whether that split matches the new target's hidden-test structure remains a
question for official data/rules and the validation role. No training result,
submission or leaderboard improvement is asserted by this example.

Other scenarios: `otto`, `rogii`, `amex`, `m5`. See
[the complete host workflow](../../skills/kaggle-solutions-skills/references/multi-agent-research.md)
and [scenario registry](../../skills/kaggle-solutions-skills/assets/scenarios.json).
