# Code Walkthrough & Architecture Guide: "How We Did It"

> **Purpose of this Guide**: If your professor asks you to open the codebase, share your screen, or explain *"How did you implement this in code?"*, this document gives you the exact file names, line numbers, simple English explanations, and winning answers. You will never get stuck!

---

## 🗺️ Project Directory Map (At a Glance)

Here is where everything lives in the repository (`c:\dev\CN_Project`):

```
c:\dev\CN_Project\
├── data/
│   ├── metadata/
│   │   └── dataset_statistics.json      <- Flow duration stats & class counts
│   └── processed/
│       ├── iscx_flows.csv               <- 3,000 extracted flows (ISCX VPN 2016)
│       └── ustc_flows.csv               <- 3,000 extracted flows (USTC-TFC 2016)
├── figures/                             <- ALL 8 publication-grade 300 DPI figures
├── results/                             <- ALL raw experiment CSV tables (CV, ablation, SOTA)
├── src/
│   ├── dataset_loader.py                <- [Step 1] PCAP parsing & 8-feature extraction
│   ├── models.py                        <- [Step 2] FFNN (325 params), CNN, LSTM, Transformer, & Fitness F
│   ├── mopso_optimizer.py               <- [Step 3] Swarm optimization, Pareto archive & Page-Hinkley drift
│   ├── run_experiments.py              <- [Step 4] 10-fold CV, paired t-tests, ablation, & feature importance
│   └── generate_visual_representations.py <- [Step 5] Plots all 8 figures
├── tests/                               <- 13 pytest tests (100% passing)
├── docs/                                <- Presentation slides, paper updates, and guides
├── README.md                            <- Package documentation & quickstart
└── pytest.ini                           <- Test suite configuration
```

---

---

## 🔍 Module 1: `src/dataset_loader.py` — How PCAP Ingestion & Feature Extraction Works

### 1. What this file does in plain English:
*"This script takes raw `.pcap` packet capture files from ISCX and USTC, groups individual packets into bidirectional 'flows' (conversations between two devices), and calculates the exact 8 network features needed by our neural network."*

### 2. Key Code Sections to Show Your Faculty:
- **Grouping packets into flows (5-Tuple)**:
  - Lines 40–55: We use Scapy's `PcapReader` to stream packets without crashing RAM.
  - A bidirectional flow key is defined by the 5-tuple:
    ```python
    # Two directions of the same conversation share the same flow key
    flow_key = tuple(sorted([(src_ip, src_port), (dst_ip, dst_port)])) + (protocol,)
    ```
- **Calculating the 8 Standard Features**:
  - Look at lines 60–110 in `extract_flow_features()`:
    1. `inter_arrival_time` ($\Delta t$): `np.diff(timestamps).mean()` — average time between consecutive packets.
    2. `packet_size`: `np.mean(packet_lengths)` — average payload size in bytes.
    3. `protocol`: IP protocol number (`6` for TCP, `17` for UDP).
    4. `flow_duration`: `timestamps[-1] - timestamps[0]` — total active connection time in seconds.
    5. `total_bytes`: `np.sum(packet_lengths)` — total volume transferred.
    6. `packet_count`: `len(packets)` — total number of packets in the flow.
    7. `dst_port`: destination port (e.g. 443, 80).
    8. `ttl`: `np.mean(ttls)` — Time-to-Live hop counter from the IP header.
- **Balanced Class Sampling (600 per class)**:
  - Lines 120–150: Collects exactly 600 flows per class to make a balanced 3,000-sample dataset, matching our senior's 3,000-sample baseline.
  - Saves the output to `data/processed/iscx_flows.csv` and `data/processed/ustc_flows.csv`.

### 3. If Your Faculty Asks:
> **Faculty**: *"Did you normalize the data globally before splitting into folds?"*  
> **Your Answer**: *"No, Professor. Normalizing before splitting is a classic data leakage mistake. In our code, raw features are saved directly to CSV. Normalization with `StandardScaler` is done **strictly inside each training fold** during cross-validation in `src/run_experiments.py`."*

---

---

## 🔍 Module 2: `src/models.py` — The Neural Network Architectures & 5-Component Fitness ($F$)

### 1. What this file does in plain English:
*"This file defines our lightweight 325-parameter Feed-Forward Neural Network (`FFNN`), the three PyTorch Deep Learning baselines (1D-CNN, LSTM, Transformer), and the mathematical formula for Composite Overhead $F$."*

### 2. Key Code Sections to Show Your Faculty:
- **How the 325 parameters of FFNN are calculated**:
  - Look at line 30–35:
    ```python
    class FFNN:
        def __init__(self, ni=8, h1=16, h2=8, no=5):
            # 8 inputs -> 16 hidden1 -> 8 hidden2 -> 5 outputs
            # Weights: (8*16) + (16*8) + (8*5) = 128 + 128 + 40 = 296
            # Biases:  16 + 8 + 5 = 29
            # Total parameters D = 296 + 29 = 325!
            self.D = 325
    ```
  - *Why this is cool*: In lines 36–50, the neural network forward pass is implemented directly in pure NumPy (`@` matrix multiplication + ReLU activation + Softmax). It has zero PyTorch bloat and runs in microseconds!
- **How the 5-Component Fitness $F$ is calculated**:
  - Look at lines 60–93 in `FFNN.composite(X, y, w, weights)`:
    $$F = \alpha \cdot f_1 + \beta \cdot f_2 + \gamma \cdot f_3 + \delta \cdot f_4 + \epsilon \cdot f_5$$
    1. `f1_err`: Classification error $= 1.0 - \text{accuracy}$.
    2. `f2_frur` (Flow Rule Update Rate / Jitter): We add Gaussian noise $\sigma=0.10$ to the inputs and measure how often the predicted class flips. Lower means more stable OpenFlow rules!
    3. `f3_cpu` (Switch CPU load): Percentage of weights whose absolute value exceeds $0.3$ (`np.mean(np.abs(w) > 0.3)`). Denser weights require more CPU multiply operations.
    4. `f4_fsd` (Flow Setup Delay): Mean absolute weight magnitude (`np.mean(np.abs(w)) / 3.0`). Larger weights take longer to set up in switch TCAM tables.
    5. `f5_bw` (Southbound Bandwidth): Percentage of non-zero sparse weights (`np.mean(np.abs(w) > 0.05)`). Fewer weights mean smaller OpenFlow messages sent over the controller link.
- **The 3 Deep Learning Baselines**:
  - Look at lines 98–156:
    - `PyTorchCNN1D`: 2 Conv1d layers + BatchNorm + AdaptiveAvgPool + Linear classifier (**2,373 parameters**).
    - `PyTorchLSTM`: 2-layer Bidirectional LSTM + Linear head (**13,093 parameters**).
    - `PyTorchTransformer`: Embedding + 2-layer Multi-Head Attention Encoder (4 heads, 64 feedforward) + Linear head (**18,437 parameters**).
    - Wrapped uniformly in `DeepLearningWrapper` (line 161) so they can be trained with Adam and cross-entropy loss.

### 3. If Your Faculty Asks:
> **Faculty**: *"How do you test the stability of flow rules (FRUR) in code?"*  
> **Your Answer**: *"In `f2_frur()` at line 66, we inject slight jitter noise into packet arrival times and payload sizes ($X + \mathcal{N}(0, \sigma^2)$). If a model is brittle, small network noise causes it to constantly change its classification, which would flood the OpenFlow switch with rule updates. We measure the rate of classification flips across 5 trials."*

---

---

## 🔍 Module 3: `src/mopso_optimizer.py` — Particle Swarm & Page-Hinkley Drift Detector

### 1. What this file does in plain English:
*"This file implements the Multi-Objective Particle Swarm Optimization (MOPSO) algorithm that trains our neural network without backpropagation, maintains a menu of non-dominated solutions (Pareto front), and detects concept drift using the Page-Hinkley test."*

### 2. Key Code Sections to Show Your Faculty:
- **What is a Particle?**:
  - In our code, each particle is a candidate set of 325 weights: $\mathbf{X}_i \in \mathbb{R}^{325}$.
  - The swarm consists of 45 particles exploring the weight space.
- **Clerc's Constriction Velocity Update**:
  - Velocity update rule:
    $$V_i(t+1) = \omega V_i(t) + c_1 r_1 (\text{pbest}_i - X_i) + c_2 r_2 (\text{gbest} - X_i)$$
    with standard Clerc constriction coefficients: $\omega = 0.7298$, $c_1 = 1.49618$, $c_2 = 1.49618$.
- **Pareto Dominance Check in Code**:
  - Look at lines 35–50 in `dominates(costA, costB)`:
    ```python
    # Objective 1: Classification Error (f1)
    # Objective 2: Composite Overhead (F)
    # Solution A dominates B if A is <= B on both objectives, AND strictly < on at least one!
    def dominates(costA, costB):
        return (costA[0] <= costB[0] and costA[1] <= costB[1]) and \
               (costA[0] < costB[0] or costA[1] < costB[1])
    ```
- **External Archive with Crowding Distance**:
  - Lines 60–110: An external archive retains up to 40 non-dominated solutions. When the archive exceeds 40, it calculates the *crowding distance* (diversity) and removes crowded solutions to preserve a wide spread of choices.
- **Knee Point Selection (`deploy_knee`)**:
  - Line 145: Automatically finds the solution closest to the ideal origin $(0, 0)$ in normalized $(f_1, F)$ space. That solution is deployed to the SDWN controller.
- **Page-Hinkley Drift Detector (`PageHinkley`)**:
  - Look at lines 180–220:
    - Tracks classification error $x_n = 1 - \text{acc}_n$.
    - Computes cumulative deviation: $U_n = \sum (x_k - \bar{x} - \delta)$.
    - Maintains minimum $m_n = \min_{k} U_k$.
    - If difference $U_n - m_n > \lambda$ (threshold $\lambda=2.0$), a **drift signal** is triggered!
    - When drift is detected, the optimizer performs a **warm-restart MOPSO** seeded from the current knee point, converging in under 2.5 seconds!

### 3. If Your Faculty Asks:
> **Faculty**: *"Why did you use Clerc's constriction factor values ($\omega=0.7298, c_1=c_2=1.49618$)?"*  
> **Your Answer**: *"Because under Clerc & Kennedy's mathematical convergence theory, these exact parameters guarantee that the expectation eigenvalues lie inside the unit circle ($\rho = 0.8543 < 1$) as proved in Lemma 1, and the particle variance remains strictly bounded as proved in Lemma 2. This prevents the swarm from exploding or oscillating."*

---

---

## 🔍 Module 4: `src/run_experiments.py` — 10-Fold CV, $t$-Tests, Ablation & Feature Importance

### 1. What this file does in plain English:
*"This is the master experimental engine. It runs the 10-fold cross-validation, executes paired $t$-tests to compute $p$-values, performs the 3-policy weight ablation, and computes permutation feature importance."*

### 2. Key Code Sections to Show Your Faculty:
- **10-Fold Stratified Cross-Validation (Leakage-Free)**:
  - Look at lines 50–75:
    ```python
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    for fold, (train_idx, test_idx) in enumerate(skf.split(X_raw, y)):
        X_tr_raw, y_tr = X_raw[train_idx], y[train_idx]
        X_te_raw, y_te = X_raw[test_idx], y[test_idx]
        
        # Log-transform continuous features
        X_tr_log = np.log1p(np.maximum(X_tr_raw, 0.0))
        X_te_log = np.log1p(np.maximum(X_te_raw, 0.0))
        
        # Scaler is FIT STRICTLY on train fold ONLY!
        scaler = StandardScaler()
        X_tr = scaler.fit_transform(X_tr_log)
        X_te = scaler.transform(X_te_log)  # Only transform test fold!
    ```
- **Paired $t$-Test & Exact $p$-Values**:
  - Look at lines 155–170:
    ```python
    # Paired two-tailed t-test between MOPSO and PSO across the 10 paired folds
    t_stat, p_val = stats.ttest_rel(df_mopso["accuracy"], df_pso["accuracy"])
    ```
    - Yields exact $p = 0.0028 < 0.01$ for USTC and $p = 0.0030 < 0.01$ for ISCX, proving statistical significance!
- **3-Policy Fitness Weight Ablation**:
  - Look at lines 210–260 in `run_ablation_study()`:
    - Defines the 4 weight scenarios:
      1. Default: $\alpha=0.45, \beta=0.20, \gamma=0.15, \delta=0.10, \epsilon=0.10$
      2. Accuracy-Critical: $\alpha=0.80, \beta=0.08, \gamma=0.06, \delta=0.03, \epsilon=0.03$
      3. Bandwidth-Constrained: $\alpha=0.25, \beta=0.10, \gamma=0.10, \delta=0.05, \epsilon=0.50$
      4. Latency-Sensitive: $\alpha=0.25, \beta=0.10, \gamma=0.10, \delta=0.50, \epsilon=0.05$
    - Runs MOPSO under each policy and saves the resulting Pareto solution counts and $F$-ranges to `results/ablation_policies_*.csv`.
- **Permutation Feature Importance**:
  - Look at lines 305–350 in `run_feature_importance()`:
    - For each of the 8 features, it randomly shuffles that feature column across test samples:
      ```python
      X_perm = X_te.copy()
      X_perm[:, f_idx] = np.random.permutation(X_perm[:, f_idx])
      perm_acc = ffnn.acc(X_perm, y_te, best_w)
      perm_F = ffnn.composite(X_perm, y_te, best_w)[0]
      acc_drop = baseline_acc - perm_acc
      ```
    - Measures which feature causes the largest performance drop when corrupted!

---

---

## 🔍 Module 5: `src/generate_visual_representations.py` — Generating the 8 Figures

### 1. What this file does in plain English:
*"This script takes all the calculated numbers and CSV files and generates 8 high-resolution, 300-DPI publication charts. Every figure is saved as a clean `.png` inside the `figures/` folder."*

### 2. How Each Function Maps to an Instruction:
- `plot_instruction_1()` $\to$ `figures/fig_inst1_dataset_durations.png` (Flow durations on log scale & class balance).
- `plot_instruction_2()` $\to$ `figures/fig_inst2_dl_params_overhead.png` (Parameter bloat: 325 vs 18,437 & real accuracy).
- `plot_instruction_3()` $\to$ `figures/fig_inst3_cv_bars_ustc.png` & `figures/fig_inst3_cv_bars_iscx.png` (10-fold CV grouped bars with standard deviation error bars and red $p$-value significance brackets).
- `plot_instruction_4()` $\to$ `figures/fig_inst4_ablation_policy_bars.png` (Pareto menu counts & deployed overhead $F$).
- `plot_instruction_5()` $\to$ `figures/fig_inst5_feature_importance_comparison.png` (Side-by-side horizontal bars for USTC vs ISCX).
- `plot_instruction_6()` $\to$ `figures/fig_inst6_lemma_stability.png` (Complex plane unit circle showing eigenvalues $\rho = 0.8543 < 1.0$ and variance decay curve).
- `plot_instruction_7()` $\to$ `figures/fig_inst7_discussion_tradeoffs.png` (5-axis radar chart showing holistic SDN operational advantages).
- `plot_instruction_8()` $\to$ `figures/fig_inst8_system_pipeline.png` (End-to-end architecture card diagram).

---

---

## 🔍 Module 6: `tests/` — How the Unit Test Suite Works

### 1. What this folder does:
*"Contains 13 automated tests written with `pytest`. These tests prove that our mathematical formulas, model parameters, and anti-leakage rules work properly before any experiment is run."*

### 2. What Each Test Verifies:
1. `tests/test_dataset_pipeline.py`:
   - Checks that 8 features are strictly present.
   - Proves zero data leakage: scaler parameters are not shared across folds.
2. `tests/test_models.py`:
   - Verifies the exact parameter count $D=325$ for FFNN.
   - Verifies 1D-CNN ($D=2,373$), LSTM ($D=13,093$), and Transformer ($D=18,437$).
   - Verifies forward pass output shapes ($[N, 5]$).
3. `tests/test_composite_fitness.py`:
   - Verifies the 5-component fitness calculation $F \in [0, 1]$.
   - Verifies that FRUR jitter injection properly measures sensitivity.
4. `tests/test_mopso_optimizer.py`:
   - Verifies Pareto dominance logic.
   - Verifies external archive capacity constraint ($A_{\text{max}} = 40$).
   - Verifies Page-Hinkley drift detection triggers when error accumulates.

### 3. How to Run Live in Front of Faculty:
Open terminal in `c:\dev\CN_Project` and run:
```bash
uv run pytest tests/
```
Output to show them:
```
============================= 13 passed in 13.40s =============================
```

---

---

## 🎯 Quick Cheat-Sheet: "If Professor Points to X, Say Y"

| Professor's Question | Where It Is in Code | What You Say (Plain English) |
|---|---|---|
| *"Where are your 8 features extracted?"* | `src/dataset_loader.py` line 60 | *"In `extract_flow_features()`, we calculate IAT, packet size, protocol, duration, total bytes, packet count, dst port, and TTL from the Scapy packet stream."* |
| *"Where do you prove your model has only 325 parameters?"* | `src/models.py` line 34 | *"In `FFNN.__init__()`, $8 \times 16 + 16 + 16 \times 8 + 8 + 8 \times 5 + 5 = 325$ weights and biases."* |
| *"How is composite fitness $F$ calculated?"* | `src/models.py` line 81 | *"In `FFNN.composite()`, we combine error $f_1$, FRUR jitter $f_2$, CPU density $f_3$, setup delay $f_4$, and bandwidth $f_5$ with weights summing to 1.0."* |
| *"Where is the Pareto dominance logic?"* | `src/mopso_optimizer.py` line 35 | *"In `dominates()`, solution A dominates B if A is less than or equal to B on both error and overhead, and strictly smaller on at least one."* |
| *"Where is concept drift detected?"* | `src/mopso_optimizer.py` line 180 | *"In `PageHinkley.update()`, it accumulates error rate deviations and flags drift when $U_n - m_n > 2.0$."* |
| *"Where is the paired $t$-test calculated?"* | `src/run_experiments.py` line 155 | *"We use `scipy.stats.ttest_rel()` across the 10 paired validation folds to obtain the exact $p$-value ($p = 0.0028$)."* |
| *"How did you generate these figures?"* | `src/generate_visual_representations.py` | *"We wrote a standalone matplotlib script that reads our experimental CSVs and plots publication-grade 300 DPI figures."* |

You are now 100% prepared to explain any line of code, show any test, and defend your work with complete confidence!

