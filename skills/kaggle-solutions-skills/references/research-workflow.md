# Research and transfer

Use this when selecting source material or proposing experiments. Keep the output proportional to the request; a single-method question does not need a complete dossier.

## Similarity is about structure

Compare candidates on these dimensions:

| Dimension | Questions that change a decision |
|---|---|
| Prediction unit | Row, customer, essay span, recording window, study, item/session, trajectory or entire game? |
| Hidden data | New entities, future periods, novel identities, new acquisition sites, evolving opponents? |
| Metric | Probability quality, ranking, thresholded overlap, weighted aggregates or win/rating? |
| Information boundary | What is visible at inference, and what must be estimated independently? |
| Constraint | CPU/GPU, memory, dependency/network access, duration and submission format? |
| Available signal | Reference sequence, geometry, unlabeled data, pretrained models, temporal history? |

Explain which dimensions match and which do not. Archive categories such as Featured/Research/Playground are competition kinds, not data modalities. Heuristic modality tags may be incomplete or wrong.

Useful queries:

```text
python <skill-dir>/scripts/solutions.py show m5-forecasting-accuracy --json
python <skill-dir>/scripts/solutions.py search "credit default" --modality tabular --top-rank 5
python <skill-dir>/scripts/solutions.py search "agent" --modality simulation
python <skill-dir>/scripts/solutions.py patterns "validation" --json
python <skill-dir>/scripts/solutions.py patterns "retrieval" --json
```

For a technique request, `patterns --json` supplies the evidence locators, applicability and minimal experiments. Metadata search can return a competition because of a lexical overlap even when it has no evidence for that technique.

## A useful extraction

For each consequential choice record:

`source and locator → observed choice → reported effect or unknown → conditions → transfer hypothesis → minimal comparison`.

Read the relevant training/inference code when the writeup leaves a fragile implementation detail unclear: grouping key, hidden-test preprocessing, loss/metric transform, class order, pseudo-label generation, stage-one OOF, model version or action transformation. Do not infer execution from comments, notebook titles, inactive feature switches or an unrun notebook cell.

Favor a cheap experiment whose result can change the next decision. A method can be useful because it improves quality, robustness, runtime, memory or explanatory value. Costs and unsupported assumptions belong beside the proposed benefit.

## Existing knowledge-card routes

Search `assets/knowledge/patterns.json` through the CLI rather than loading the entire archive:

- Validation: `temporal-horizon-validation`, `entity-aligned-validation`, `metric-proxy-audit`.
- Tabular: `tabular-history-features`.
- Recommenders: `retrieval-then-ranking`, `pipeline-ablation`.
- Text/pseudo labels: `pseudo-label-fold-isolation`, `ensemble-distillation`.
- Audio: `audio-context-alignment`, `source-quality-audit`, `inference-budget`.
- Vision: `localize-then-classify`, `stage-error-augmentation`, `open-set-identity`.
- Simulation: `simulation-opponent-diversity`, `simulation-runtime-fallback`.
- Structured/domain models: `domain-alignment-grid`, `reliability-aware-routing`, `controller-residual-matching`.
- Ensembles/optimization: `ensemble-marginal-gain`, `iterated-local-search`.

These routes identify seed examples, not an exhaustive modality handbook. Changes in cards should update this list when useful.

## Handoff to competition execution

Hand off the current baseline identity, official objective, validation assumptions, legal data inputs, proposed change/control, relevant source versions, expected resource budget and what observation would affect the next decision. Leave split construction, model execution, artifact validation and submission endgame with the chosen execution workflow. Respect existing scope: if the user asked only for research, finish the research.

If execution results return, record the exact context: split/data/source version, seed(s), experiment configuration, measured score and resource use, error subgroups and failed attempts. A supported failure often creates a more useful card than another unqualified success.
