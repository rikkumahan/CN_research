# Review 2 — MOPSO-FFNN-AD Strengthening Plan

## 0. Mission

Strengthen the senior's **MOPSO-FFNN-AD** research work for Review 2 by replacing the synthetic evaluation with public real-world traffic benchmarks, adding controlled deep-learning baselines, statistical validation, deployment-policy ablation, feature importance, discussion, and reproducible packaging.

**Deadline:** tomorrow morning.

## 1. Source files

Use these as the primary source of truth:

- Base paper: `IET Communications - 2022 - Pradhan - A neuro‐evolutionary approach for software defined wireless network traffic (1) (1).pdf`
- Senior paper: `budithi.pdf`
- Senior implementation: `MOPSO_FFNN_AD_FINAL - Budithi Supraja 25MAI0030.py`

Do not invent experimental results. Clearly label old/synthetic results as historical results and new real-dataset results as new experiments.

## 2. Current senior implementation

The current senior system uses:

- FFNN architecture: **8 → 16 → 8 → 5**
- Trainable parameters: **D = 325**
- Eight input features:
  1. inter-arrival time
  2. packet size
  3. protocol type
  4. flow duration
  5. total bytes
  6. packet count
  7. destination port
  8. TTL
- Composite objective:
  `F = alpha*f1 + beta*FRUR + gamma*CPU + delta*FSD + epsilon*BW`
- Current default weights:
  - alpha = 0.45
  - beta = 0.20
  - gamma = 0.15
  - delta = 0.10
  - epsilon = 0.10
- Page-Hinkley drift detection is based on error rate `1 - accuracy`.
- Existing code already contains PSO, MOPSO, Pareto archive, drift simulation, figures, confusion matrices, and result printing.

## 3. Review 2 requirements

### R1 — Real datasets
Use:
- ISCX VPN/non-VPN 2016
- USTC-TFC 2016

Build a reproducible PCAP/flow preprocessing pipeline that extracts the exact eight features above.

Deliver:
- processed dataset files
- class counts
- total samples
- flow-duration statistics
- dataset subsection/table

### R2 — Deep learning baselines
Implement and run:
- CNN (1D)
- LSTM
- a small/simple Transformer (ET-BERT is optional; a simpler Transformer is acceptable)

All models must use the same real datasets and equivalent input features.

Report:
- Accuracy
- parameter count
- training time where feasible
- comparable composite overhead `F`

### R3 — 10-fold stratified cross-validation
Run 10-fold stratified CV on real datasets.

For important models report:
- mean Accuracy ± std
- mean F ± std
- paired t-test against PSO-FFNN
- p-values

Do not fabricate significance. If p >= 0.05, report it honestly.

### R4 — Fitness-weight ablation
Evaluate three deployment policies:
1. Accuracy-critical: alpha = 0.8
2. Bandwidth-constrained: epsilon = 0.5
3. Latency-sensitive: delta = 0.5

The remaining weights must be explicitly documented. Prefer a normalized set summing to 1 unless the source protocol requires otherwise.

Deliver:
- Pareto front figure comparing policies
- short interpretation of how the front shifts

### R5 — Feature importance
Use permutation importance or Garson-style analysis.

Identify the contribution of all 8 features.

Deliver:
- numeric feature-importance table
- bar chart

### R6 — Stability
Correctly typeset and explain Lemmas 1 and 2 from the source material.

Explain:
- first-order convergence
- second-order/variance convergence
- why stability matters for SDWN controller behavior

Do not silently alter mathematical meaning.

### R7 — Discussion
Discuss:
1. engineered flow features vs raw packet bytes
2. MOPSO training time vs simple SGD
3. generalization concerns for QUIC/TLS 1.3

Do not claim QUIC/TLS 1.3 performance unless experimentally evaluated.

### R8 — Reproducibility
Package:
- preprocessing
- models
- MOPSO/PSO
- Mininet scripts if present
- experiments
- result generation
- README
- appendix with hyperparameter grids
- full confusion matrices

## 4. Execution order

Follow this order exactly:

1. Inspect and run current senior code.
2. Build and validate ISCX/USTC preprocessing.
3. Integrate real datasets into FFNN/PSO/MOPSO.
4. Run baseline sanity checks.
5. Implement CNN/LSTM/Transformer.
6. Implement one reusable evaluation interface for all models.
7. Run 10-fold CV + statistical tests.
8. Run deployment-policy ablation.
9. Run feature importance.
10. Generate final tables/figures.
11. Update paper sections.
12. Package repository + README + appendix.

## 5. Hard rules

- Never fabricate numbers.
- Never copy literature accuracy into a same-dataset result table unless explicitly labeled as literature.
- Never claim that a model "outperforms" another without direct comparable experiments.
- Avoid data leakage.
- Fit normalization only on training data within each fold.
- Keep the test fold unseen during training/model selection.
- Preserve labels and dataset provenance.
- Save raw fold-level results before aggregating.
- Save configuration and random seed for every experiment.
- Do not overwrite old results; put new real-dataset results in a separate output directory.
- If a requirement cannot be completed rigorously before the deadline, document the limitation rather than fabricating evidence.

## 6. Minimum acceptable overnight target

At minimum produce:

- real ISCX and USTC processed datasets
- PSO-FFNN and MOPSO-FFNN-AD real-data results
- CNN, LSTM, Transformer baseline results
- Accuracy + F
- 10-fold CV summary
- paired t-tests
- 3-policy Pareto figure
- feature-importance figure
- updated Table 2 and Table 6
- dataset statistics table
- reproducibility README

## 7. Working style

Work incrementally. After each milestone:

- run a small smoke test
- validate shapes and labels
- save outputs
- report exact files created
- report failures/blockers
- do not continue past a broken prerequisite

