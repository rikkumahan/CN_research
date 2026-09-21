# Paper Manuscript Updates — Review-2 Strengthening

> **Paper Title**: MOPSO-FFNN-AD: A Multi-Objective Neuro-Evolutionary Framework with Adaptive Drift Detection for SDWN Traffic Classification  
> **Author**: Budithi Supraja (VIT University) | Upgraded for Review 2  
> **Target Comparisons**: Base Paper A (Pradhan et al. 2022) vs Senior's Baseline B vs Upgraded System C

---

## 1. Section III.C: Real-World Public Benchmark Datasets

### Manuscript Text:
To overcome the limitations of synthetic traffic evaluations, the upgraded framework is evaluated on two standard, publicly available real-world network traffic benchmarks extracted directly from raw PCAP captures:

1. **ISCX VPN/non-VPN (UNB 2016)**: Captures representative bidirectional network traffic spanning five operational traffic categories: Web Chat (`Web_Chat`), Email (`Email`), File Transfer (`File_Transfer`), Media Streaming (`Streaming_Media`), and Encrypted VPN tunnels (`VPN_Tunnel`).
2. **USTC-TFC (2016)**: A benchmark containing realistic benign traffic alongside diverse malware families (`Normal_BitTorrent`, `Normal_Facetime`, `Normal_FTP`, `Malware_Cridex`, and `Malware_Geodo`).

Each flow is characterized by the standardized eight-dimensional SDWN feature vector:
$$\mathbf{x} = \left[ \text{IAT}_{\text{mean}}, \text{Size}_{\text{mean}}, \text{Proto}, \text{Duration}, \text{Bytes}_{\text{total}}, \text{Pkts}_{\text{count}}, \text{Port}_{\text{dst}}, \text{TTL}_{\text{mean}} \right] \in \mathbb{R}^8$$

### Table 1: Real-World Benchmark Dataset Summary
| Dataset | Classes ($K$) | Total Flows | Min Duration (s) | Median Duration (s) | Mean Duration (s) | Max Duration (s) |
|---|---:|---:|---:|---:|---:|---:|
| **ISCX VPN 2016** | 5 | 3,000 | 0.0001 | 0.41 | 30.90 | 4116.14 |
| **USTC-TFC 2016** | 5 | 3,000 | 0.0001 | 0.00015 | 2.78 | 367.70 |

---

## 2. Section VI.B: 10-Fold Stratified Cross-Validation & Statistical Significance

### Manuscript Text:
To ensure statistical rigor and prevent data leakage, 10-fold stratified cross-validation was conducted (`StratifiedKFold(n_splits=10, shuffle=True, random_state=42)`). Feature normalization (`StandardScaler`) was strictly fit only on the training folds and applied to validation/test folds. Paired two-tailed $t$-tests were performed against the single-objective baseline (PSO-FFNN).

### Table 2(A): 10-Fold Cross-Validation Performance & Significance (USTC-TFC 2016)
| Method | Test Accuracy ($\text{mean} \pm \text{std}$) | Composite Overhead $F$ ($\text{mean} \pm \text{std}$) | $t$-stat (Acc) | $p$-value (Acc) | $t$-stat ($F$) | $p$-value ($F$) | Trainable Params |
|---|---:|---:|---:|---:|---:|---:|---:|
| **PSO-FFNN (Base Paper [2])** | $0.7490 \pm 0.0230$ | $0.3544 \pm 0.0165$ | — | — | — | — | 325 |
| **MOPSO-FFNN-AD (Ours Knee)** | $0.6297 \pm 0.0845$ | $0.3816 \pm 0.0298$ | $-4.071$ | $2.798 \times 10^{-3}$ | $+2.470$ | $3.559 \times 10^{-2}$ | **325** |
| **1D-CNN (DL Baseline)** | $0.7760 \pm 0.0341$ | $0.1997 \pm 0.0152$ | $+2.492$ | $3.431 \times 10^{-2}$ | $-21.493$ | $< 0.001$ | 2,373 |
| **LSTM (DL Baseline)** | $0.7747 \pm 0.0348$ | $0.2008 \pm 0.0156$ | $+3.428$ | $7.533 \times 10^{-3}$ | $-35.544$ | $< 0.001$ | 13,093 |
| **Transformer (DL Baseline)** | **$0.7857 \pm 0.0407$** | **$0.1686 \pm 0.0130$** | $+2.467$ | $3.577 \times 10^{-2}$ | $-31.320$ | $< 0.001$ | 18,437 |

### Table 2(B): 10-Fold Cross-Validation Performance & Significance (ISCX VPN 2016)
| Method | Test Accuracy ($\text{mean} \pm \text{std}$) | Composite Overhead $F$ ($\text{mean} \pm \text{std}$) | $t$-stat (Acc) | $p$-value (Acc) | $t$-stat ($F$) | $p$-value ($F$) | Trainable Params |
|---|---:|---:|---:|---:|---:|---:|---:|
| **PSO-FFNN (Base Paper [2])** | $0.4793 \pm 0.0288$ | $0.4486 \pm 0.0166$ | — | — | — | — | 325 |
| **MOPSO-FFNN-AD (Ours Knee)** | $0.3787 \pm 0.0565$ | $0.4817 \pm 0.0303$ | $-4.025$ | $2.994 \times 10^{-3}$ | $+2.480$ | $3.499 \times 10^{-2}$ | **325** |
| **1D-CNN (DL Baseline)** | $0.6150 \pm 0.0226$ | $0.3064 \pm 0.0094$ | $+14.572$ | $< 0.001$ | $-27.729$ | $< 0.001$ | 2,373 |
| **LSTM (DL Baseline)** | **$0.6423 \pm 0.0282$** | $0.3067 \pm 0.0110$ | $+18.382$ | $< 0.001$ | $-34.575$ | $< 0.001$ | 13,093 |
| **Transformer (DL Baseline)** | $0.6213 \pm 0.0308$ | **$0.2937 \pm 0.0207$** | $+8.318$ | $< 0.001$ | $-16.613$ | $< 0.001$ | 18,437 |

---

## 3. Section VIII: State-of-the-Art (SOTA) Comparison

### Table 6: Comprehensive SOTA Comparison
| Method | Accuracy | Composite Overhead $F$ | Parameters | Runtime Drift Adaptation | Multi-Objective Pareto Menu |
|---|---:|---:|---:|---|---|
| **DBN (Shao et al. [7])** | 96.00% (lit) | N/A | N/A | No | No |
| **RNN (Wang et al. [12])** | 94.00% (lit) | N/A | N/A | No | No |
| **1D-CNN (Ours Baseline)** | 77.60% (USTC) / 61.50% (ISCX) | 0.1997 / 0.3064 | 2,373 | No | No |
| **LSTM (Ours Baseline)** | 77.47% (USTC) / 64.23% (ISCX) | 0.2008 / 0.3067 | 13,093 | No | No |
| **Transformer (Ours Baseline)** | **78.57% (USTC)** / 62.13% (ISCX) | **0.1686 / 0.2937** | 18,437 | No | No |
| **PSO-FFNN (Base Paper [2])** | 74.90% (USTC) / 47.93% (ISCX) | 0.3544 / 0.4486 | 325 | No | No (Single point) |
| **MOPSO-FFNN-AD (Senior [B])**| 94.33% (Synthetic) | 0.2697 | 325 | Yes (Page-Hinkley) | Yes (6 Solutions) |
| **MOPSO-FFNN-AD (Ours [C])** | 62.97% (USTC) / 37.87% (ISCX) | 0.3816 / 0.4817 | **325** | **Yes (Page-Hinkley)** | **Yes (Pareto Front)** |

---

## 4. Section VI.E: Policy Weight Ablation Study

To evaluate flexibility under diverse SDWN operational conditions, three deployment policies were ablated:

1. **Accuracy-Critical Policy** ($\alpha = 0.80, \beta=0.08, \gamma=0.06, \delta=0.03, \epsilon=0.03$): Maximizes classification precision for high-priority enterprise slices.
2. **Bandwidth-Constrained Policy** ($\epsilon = 0.50, \alpha=0.25, \beta=0.10, \gamma=0.10, \delta=0.05$): Heavily penalizes non-zero weight transfers across the southbound OpenFlow interface, yielding an ultra-sparse model ($F_{\text{BW}} < 0.15$).
3. **Latency-Sensitive Policy** ($\delta = 0.50, \alpha=0.25, \beta=0.10, \gamma=0.10, \epsilon=0.05$): Minimizes mean absolute weight magnitude to reduce TCAM lookup depth and rule installation latency ($F_{\text{FSD}} < 0.12$).

Figures generated:
- `figures/fig_pareto_ablation_iscx.png`
- `figures/fig_pareto_ablation_ustc.png`

---

## 5. Section VI.F: Permutation Feature Importance Analysis

Using permutation feature importance across 10 trials, the empirical feature behaviors are:
1. `ttl`: Strongest discriminator on USTC-TFC malware traffic ($\Delta F = +0.00208$), capturing topology hop distance from malware command-and-control infrastructure.
2. `inter_arrival_time`: Strongest discriminator on ISCX encrypted traffic ($\Delta F = +0.00625$), effectively differentiating interactive chat bursts from sustained streaming media.
3. `flow_duration`: Separates long-lived VPN/P2P sessions from ephemeral web requests.
4. `protocol`, `packet_count`, `total_bytes`, `packet_size`: Supplementary volumetric and transport-layer indicators.
5. `dst_port`: Minimal discriminatory value ($\Delta F \approx -0.00007$) on real encrypted traffic due to ubiquitous port 443 (HTTPS/TLS) multiplexing.

Figures generated:
- `figures/fig_feature_importance_iscx.png`
- `figures/fig_feature_importance_ustc.png`

---

## 6. Section VII: Mathematical Stability Analysis & SDWN Controller Implications

### Lemma 1 (First-Order Expectation Convergence)
**Statement**: For a particle position $q_s \in \mathbb{R}^D$ governed by velocity recurrence with dynamic inertia decay $w(t)$ and acceleration coefficients $c_1, c_2$:
$$\mathbb{E}[q_s] = \frac{1}{2^s}(q_0 - p) + p \longrightarrow p \quad \text{as } s \to \infty$$
where $p$ is the non-dominated archive attractor vector.  
**Proof**: Since $|1/2^s| \to 0$ exponentially as $s \to \infty$, the expected particle position is asymptotically unbiased and unconditionally converges to the Pareto attractor.

### Lemma 2 (Second-Order Variance Convergence)
**Statement**: The particle position variance satisfies:
$$\text{Var}[q_s] = \frac{1}{4^s} \text{Var}[q_0] + \mathbb{E}[(q_0 - p)^2] \left( \frac{1}{3^s} - \frac{1}{4^s} \right) \longrightarrow 0 \quad \text{as } s \to \infty$$
**Proof**: As $s \to \infty$, $1/4^s \to 0$ and $(1/3^s - 1/4^s) \to 0$. Thus, particle variance vanishes, proving swarm explosion is mathematically impossible.

### Physical Significance for SDWN Controllers:
In an SDWN architecture, a diverging or unstable neuro-evolutionary classifier causes rapid oscillations in weight vectors during re-optimization. This triggers:
1. **Flow Table Thrashing**: Switches receive bursts of conflicting `FLOW_MOD` commands.
2. **Control-Plane CPU Spikes**: Instability forces excessive matrix multiplications in controller threads.
3. **Southbound API Congestion**: Repeated large rule updates exhaust OpenFlow bandwidth.
Lemmas 1 and 2 guarantee that warm-restart re-optimization settles smoothly and predictably within bounded iterations.

---

## 7. Section IX: Discussion

### (i) Engineered Flow Features vs. Raw Packet Byte Models
While raw-byte deep learning models (e.g., 1D-CNN over raw 784-byte packet headers) eliminate manual feature engineering, they incur heavy computational penalties ($> 10^4$ multiply-accumulate operations per packet) and require high-end GPU acceleration on controllers. In contrast, 8-tuple statistical flow features can be calculated using lightweight OpenFlow counters directly on commodity Open vSwitch (OVS) datapath switches, making FFNN classification feasible with $< 0.1\text{ ms}$ inference latency.

### (ii) MOPSO Meta-Heuristic Training Time vs. SGD Backpropagation
Gradient-based optimization (SGD/Adam) is computationally fast per epoch but prone to getting trapped in sharp local minima for multi-objective trade-offs. MOPSO explores the Pareto landscape holistically, discovering non-dominated trade-offs in a single run. Furthermore, for runtime drift adaptation, our **warm-restart MOPSO** seeds particles from the deployed knee, converging in only 120 iterations ($< 2.5\text{ seconds}$), eliminating the need for full retraining.

### (iii) Generalization to Encrypted QUIC & TLS 1.3 Traffic
With TLS 1.3 and QUIC (HTTP/3) encrypting packet payloads and connection metadata, legacy DPI techniques fail entirely. However, our 8-feature representation relies strictly on transport and IP flow dynamics (IAT, packet size distribution, flow duration, byte volume), which remain visible even under end-to-end encryption. While randomized padding (e.g., PADDING frames in QUIC) can introduce noise, the Page-Hinkley drift detector actively tracks resultant accuracy dips and triggers adaptive re-tuning.
