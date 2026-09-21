# REVIEW 2 — AGENT EXECUTION INSTRUCTIONS

You are the primary coding/research execution agent for an overnight Review-2 deadline.

## Priority

Finish a defensible, reproducible experimental package by tomorrow morning.

Do not spend time on cosmetic refactoring until the experiments work.

## Phase 0 — Inspect

Before changing code:

1. Read the senior paper.
2. Read the senior Python implementation.
3. Identify:
   - data input assumptions
   - FFNN architecture
   - PSO
   - MOPSO
   - fitness components
   - drift detector
   - current outputs
4. Run the current implementation once and capture the baseline outputs.

Create:

```text
docs/CURRENT_IMPLEMENTATION_AUDIT.md
```

## Phase 1 — Data

Build the real-data preprocessing pipeline.

Requirements:
- ISCX VPN/non-VPN 2016
- USTC-TFC 2016
- exact eight-feature interface
- explicit label mapping
- validation reports

First make a tiny sample run work.

Then process the full datasets.

Create:

```text
preprocessing/
data/processed/
data/metadata/
```

## Phase 2 — Integrate FFNN / PSO / MOPSO

Reuse senior logic where valid.

Do NOT rewrite the optimizer merely for style.

Refactor only where needed to:
- load real data
- support dataset selection
- support CV
- support policy weights
- save fold results

Run a small 1-fold smoke test.

## Phase 3 — Baselines

Implement small controlled models:

- CNN-1D
- LSTM
- Transformer encoder

Keep them intentionally small enough to finish overnight.

Create a single evaluation API:

```text
train()
predict()
evaluate()
count_parameters()
measure_time()
```

## Phase 4 — F implementation

Centralize fitness code.

Make it testable.

For every model, document exactly how each component is computed.

## Phase 5 — CV

Implement one reusable 10-fold evaluation runner.

Run models sequentially.

Immediately persist fold-level results.

Never rely only on console output.

## Phase 6 — Ablation

Run three deployment policies.

Save the complete weight vector used in each run.

Generate Pareto data and figures.

## Phase 7 — Feature importance

Implement permutation importance first.

Generate the bar chart.

## Phase 8 — Paper assets

Auto-generate:
- dataset statistics
- CV summary table
- SOTA/baseline table
- ablation table
- feature importance table
- confusion matrices
- Pareto plots

## Phase 9 — Reproducibility

Create:
- README
- requirements
- run scripts
- config files
- appendix data
- experiment manifest

## Failure handling

If a full experiment is too slow:

1. estimate runtime
2. reduce model/optimizer size only with explicit documentation
3. run a smoke test
4. continue with the reduced but reproducible configuration
5. record the deviation from the senior's original settings

Never silently lower iterations and then present them as original settings.

## Evidence integrity

Absolutely forbidden:
- inventing dataset statistics
- inventing accuracy/F
- copying literature numbers as new experiments
- changing random seeds after seeing results to obtain a preferred outcome
- fabricating significant p-values
- claiming QUIC/TLS 1.3 validation without testing it

## End-of-run report

At the end produce:

```text
docs/FINAL_EXPERIMENT_STATUS.md
```

with:
- completed requirements
- incomplete requirements
- exact commands
- output files
- final tables
- known limitations
