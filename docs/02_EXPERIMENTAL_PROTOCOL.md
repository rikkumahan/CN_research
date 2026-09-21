# Review 2 — Experimental Protocol

## Objective

Compare MOPSO-FFNN-AD against PSO-FFNN and controlled deep-learning baselines on the same real datasets.

## Models

1. PSO-FFNN
2. MOPSO-FFNN-AD
3. CNN-1D
4. LSTM
5. small Transformer encoder

## Input

All models consume the same eight features:

```text
IAT, packet size, protocol, flow duration,
total bytes, packet count, destination port, TTL
```

Document any categorical encoding for protocol and any scaling.

## Metrics

### Accuracy

Use standard multiclass accuracy.

Also retain:
- macro precision
- macro recall
- macro F1
- confusion matrix

### Composite overhead F

Implement the senior-paper objective:

```text
F = alpha*(1-Accuracy) + beta*FRUR + gamma*CPU + delta*FSD + epsilon*BW
```

Default:
```text
alpha   = 0.45
beta    = 0.20
gamma   = 0.15
delta   = 0.10
epsilon = 0.10
```

Existing FFNN definitions:
- FRUR = fraction of predictions changing under feature noise
- CPU = fraction of weights with `abs(weight) > 0.3`
- FSD = normalized mean absolute weight magnitude
- BW = fraction of weights with `abs(weight) > 0.05`

For CNN/LSTM/Transformer, document a comparable parameter-density / magnitude-based proxy. Do not pretend these architectures have the exact same operational semantics as the FFNN if they do not.

## Baseline parameter reporting

Report:
- number of trainable parameters
- model size
- training time
- inference time per sample/batch if feasible

## Cross-validation

Use:

```text
StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
```

For each fold save:

```text
dataset
model
fold
accuracy
F
precision
recall
f1
training_time
params
```

Then aggregate:
- mean
- std
- 95% CI if feasible

## Statistical test

Primary requested comparison:

```text
MOPSO-FFNN-AD vs PSO-FFNN
```

Use paired fold-level measurements.

Run paired t-test separately for:
- accuracy
- F

Report:
- t statistic
- p value
- significance at 0.05

Never force p < 0.05.

## Ablation policies

### A. Accuracy-critical

Required:
```text
alpha = 0.8
```

Choose/document remaining weights so the complete weight vector is valid and reproducible.

### B. Bandwidth-constrained

Required:
```text
epsilon = 0.5
```

Choose/document remaining weights.

### C. Latency-sensitive

Required:
```text
delta = 0.5
```

Choose/document remaining weights.

Output for each policy:
- Pareto archive
- accuracy/F values
- figure
- summary table

## Feature importance

Preferred first implementation: permutation importance.

Protocol:
1. Train final FFNN on training data.
2. Evaluate baseline score.
3. Permute one feature at a time.
4. Re-evaluate.
5. Importance = performance degradation.
6. Repeat enough times to reduce noise.
7. Report mean ± std where practical.

Do not compute feature importance on a contaminated test set if it is being used for model selection.

## Figures to create

1. Pareto fronts:
   - default
   - accuracy-critical
   - bandwidth-constrained
   - latency-sensitive

2. Feature importance bar chart.

3. Optional:
   - confusion matrices
   - CV accuracy distribution
   - CV F distribution
   - training-time comparison

## Tables to create

### Dataset table
Real dataset statistics.

### Updated Table 2
Suggested:

| Method | Accuracy mean ± std | F mean ± std | Accuracy p-value vs PSO | F p-value vs PSO |
|---|---:|---:|---:|---:|

### Updated Table 6

| Method | Accuracy | F | Params | Drift | Multi-objective |
|---|---:|---:|---:|---|---|
| CNN-1D | | | | No | No |
| LSTM | | | | No | No |
| Transformer | | | | No | No |
| PSO-FFNN | | | | No | No |
| MOPSO-FFNN-AD | | | | Yes | Yes |

Literature values, if included, must be marked as literature and must not be mixed with same-dataset experimental values.

## Reproducibility

Every experiment should save:
- config JSON
- seed
- dataset version/path
- fold number
- model configuration
- results CSV
- logs

Suggested:

```text
results/
├── raw/
├── aggregated/
├── figures/
├── tables/
└── configs/
```
