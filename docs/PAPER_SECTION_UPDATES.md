# Paper Manuscript Updates — Review-3 / Q2 Journal Revision

> **Paper Title**: On the Limitations of Multi-Objective Neuro-Evolutionary Traffic Classification in SDWNs: A Negative Result and Lessons Learned  
> **Target Venue**: Q2 Journal Submission (Merged Senior & Team Work)  
> **Comparative Architecture**: Base Paper A (Pradhan et al. 2022) vs Senior's Baseline B (Budithi 2024) vs Upgraded Real Evaluation C (Ours)

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

## 2. Section VI.B: 10-Fold Cross-Validation & Statistical Significance (Pareto Domination Analysis)

### Manuscript Text:
To ensure statistical rigor and prevent data leakage, 10-fold cross-validation was conducted. Feature normalization (`StandardScaler`) was strictly fit only on the training folds and applied to validation/test folds. Paired two-tailed $t$-tests were performed against the single-objective baseline (PSO-FFNN).

Crucially, empirical evaluation demonstrates that the proposed **MOPSO-FFNN-AD is strictly Pareto-dominated** by all deep learning baselines across both accuracy AND composite overhead $F$:

### Table 2(A): 10-Fold Cross-Validation Performance & Significance (USTC-TFC 2016)
| Method | Test Accuracy ($\text{mean} \pm \text{std}$) | Composite Overhead $F$ ($\text{mean} \pm \text{std}$) | $t$-stat (Acc) | $p$-value (Acc) | $t$-stat ($F$) | $p$-value ($F$) | Trainable Params |
|---|---:|---:|---:|---:|---:|---:|---:|
| **PSO-FFNN (Base Paper [2])** | $0.7490 \pm 0.0230$ | $0.3544 \pm 0.0165$ | — | — | — | — | 325 |
| **MOPSO-FFNN-AD (Proposed)** | $0.6297 \pm 0.0845$ | $0.3816 \pm 0.0298$ | $-4.071$ | $2.798 \times 10^{-3}$ | $+2.470$ | $3.559 \times 10^{-2}$ | **325** |
| **1D-CNN (DL Baseline)** | $0.7760 \pm 0.0341$ | $0.1997 \pm 0.0152$ | $+2.492$ | $3.431 \times 10^{-2}$ | $-21.493$ | $< 0.001$ | 2,373 |
| **LSTM (DL Baseline)** | $0.7747 \pm 0.0348$ | $0.2008 \pm 0.0156$ | $+3.428$ | $7.533 \times 10^{-3}$ | $-35.544$ | $< 0.001$ | 13,093 |
| **Transformer (DL Baseline)** | **$0.7857 \pm 0.0407$** | **$0.1686 \pm 0.0130$** | $+2.467$ | $3.577 \times 10^{-2}$ | $-31.320$ | $< 0.001$ | 18,437 |

### Table 2(B): 10-Fold Cross-Validation Performance & Significance (ISCX VPN 2016)
| Method | Test Accuracy ($\text{mean} \pm \text{std}$) | Composite Overhead $F$ ($\text{mean} \pm \text{std}$) | $t$-stat (Acc) | $p$-value (Acc) | $t$-stat ($F$) | $p$-value ($F$) | Trainable Params |
|---|---:|---:|---:|---:|---:|---:|---:|
| **PSO-FFNN (Base Paper [2])** | $0.4793 \pm 0.0288$ | $0.4486 \pm 0.0166$ | — | — | — | — | 325 |
| **MOPSO-FFNN-AD (Proposed)** | $0.3787 \pm 0.0565$ | $0.4817 \pm 0.0303$ | $-4.025$ | $2.994 \times 10^{-3}$ | $+2.480$ | $3.499 \times 10^{-2}$ | **325** |
| **1D-CNN (DL Baseline)** | $0.6150 \pm 0.0226$ | $0.3064 \pm 0.0094$ | $+14.572$ | $< 0.001$ | $-27.729$ | $< 0.001$ | 2,373 |
| **LSTM (DL Baseline)** | **$0.6423 \pm 0.0282$** | $0.3067 \pm 0.0110$ | $+18.382$ | $< 0.001$ | $-34.575$ | $< 0.001$ | 13,093 |
| **Transformer (DL Baseline)** | $0.6213 \pm 0.0308$ | **$0.2937 \pm 0.0207$** | $+8.318$ | $< 0.001$ | $-16.613$ | $< 0.001$ | 18,437 |

*Scientific Takeaway*: The multi-objective formulation does not produce Pareto-optimal solutions against deep learning baselines. On ISCX VPN 2016, Transformer ($62.13\%$, $F=0.2937$) and LSTM ($64.23\%$, $F=0.3067$) achieve dramatically higher accuracy while reporting lower composite overhead $F$ than MOPSO ($37.87\%$, $F=0.4817$). This establishes empirical Pareto domination.

---

## 3. Section VIII: State-of-the-Art (SOTA) Comprehensive Comparison

### Table 6: Comprehensive SOTA Benchmark Comparison
| Method | Category / Priority | Trainable Params | USTC Accuracy | ISCX Accuracy | USTC Overhead $F$ | ISCX Overhead $F$ | Concept Drift? | Multi-Objective? |
|---|:---:|---:|---:|---:|---:|---:|:---:|:---:|
| **ET-BERT (Lin et al. 2022)** | Published SOTA (Cite) | $\approx 50\text{M}$ | $96.95\%$ | — | N/A | N/A | No | No |
| **YaTC (Chen et al. 2023)** | Published SOTA (Cite) | $\approx 30\text{M}$ | $97.86\%$ | — | N/A | N/A | No | No |
| **FS-Net (Liu et al. 2019)** | Published SOTA (Cite) | $\approx 10\text{M}$ | $87.05\%$ | $52.03\%$ | N/A | N/A | No | No |
| **FlowPic (Shapira 2021)** | Published SOTA (Cite) | $\approx 2\text{M}$ | $> 90.0\%$ | $> 85.0\%$ | N/A | N/A | No | No |
| **TFE-GNN (Shen et al. 2023)** | Published SOTA (Cite) | $\approx 5\text{M}$ | $97.47\%$ | $91.92\%$ | N/A | N/A | No | No |
| **Transformer (Ours Baseline)**| Generic DL Baseline | $18,437$ | $78.57\%$ | $62.13\%$ | $0.1686$ | $0.2937$ | No | No |
| **LSTM (Ours Baseline)** | Generic DL Baseline | $13,093$ | $77.47\%$ | $64.23\%$ | $0.2008$ | $0.3067$ | No | No |
| **1D-CNN (Ours Baseline)** | Generic DL Baseline | $2,373$ | $77.60\%$ | $61.50\%$ | $0.1997$ | $0.3064$ | No | No |
| **PSO-FFNN (Base Paper [2])** | Single-Objective Baseline | $325$ | $74.90\%$ | $47.93\%$ | $0.3544$ | $0.4486$ | No | No |
| **MOPSO-FFNN-AD (Senior [1])**| Synthetic Only (Budithi)| $325$ | $94.33\%$ (synth)| N/A | $0.2697$ | N/A | Yes (PH) | Yes (6 Sols) |
| **MOPSO-FFNN-AD (Proposed)** | Proposed Framework | $325$ | $62.97\%$ | $37.87\%$ | $0.3816$ | $0.4817$ | Yes (PH) | Yes (Pareto) |

*Analysis of the Performance Gap*:
1. **Re-implementation vs. Published SOTA**: Published SOTA methods achieve $87\% - 98\%$ through large pre-trained contextual representations (ET-BERT) or 2D traffic images (FlowPic). Our re-implemented generic DL models achieve $62\% - 78\%$, demonstrating that even un-tuned deep learning easily outperforms the 325-parameter FFNN.
2. **Failure of the Synthetic Assumption**: The senior paper's reported $94.33\%$ accuracy was an artifact of synthetic Gaussian clusters. When evaluated on real-world encrypted traffic, the method underperforms significantly.

---

## 4. Section VI.E: Policy Weight Ablation Study

To evaluate how Pareto fronts shift under varying operational requirements, three deployment policies were ablated alongside default weights:
1. **Accuracy-Critical Policy** ($\alpha = 0.80, \beta=0.08, \gamma=0.06, \delta=0.03, \epsilon=0.03$)
2. **Bandwidth-Constrained Policy** ($\epsilon = 0.50, \alpha=0.25, \beta=0.10, \gamma=0.10, \delta=0.05$)
3. **Latency-Sensitive Policy** ($\delta = 0.50, \alpha=0.25, \beta=0.10, \gamma=0.10, \epsilon=0.05$)

*Finding*: Although varying policy weights shifts the relative emphasis between setup delay and bandwidth, none of the generated Pareto solutions can beat deep learning baselines in accuracy or composite overhead.

---

## 5. Section VI.F: Revised Feature Set Analysis

Permutation feature importance across 10 trials revealed:
1. **`dst_port` is Ineffective**: Ranked dead last ($\Delta F \approx -0.00007$) because modern applications tunnel over port 443 (HTTPS/TLS). It should be omitted from primary feature extraction.
2. **`ttl` is Topology-Dependent**: While ranking high on USTC ($\Delta F = +0.00208$), TTL reflects specific testbed hops and is easily spoofed or altered by intermediate middleboxes.
3. **Need for Higher-Order IAT Moments**: Standard mean IAT misses packet timing variance. FlowPic and FS-Net succeed by utilizing variance, skewness, and kurtosis of inter-arrival times.

---

## 6. Appendix A: Mathematical Stability Analysis vs. Classifier Efficacy

### Main Text Clarification:
> *"We formally prove that the MOPSO optimizer is mathematically stable with a bounded spectral radius $\rho < 1.0$ (Lemma 1) and vanishing position variance (Lemma 2, Appendix A). However, stability is an intrinsic property of the particle swarm dynamics, not of classification performance. Mathematical convergence to a Pareto-optimal point does not guarantee competitive accuracy against deep learning baselines when the underlying architecture lacks sufficient capacity."*

### Summary of Moved Lemmas (Now in Appendix A):
- **Lemma 1 (First-Order Expectation Convergence)**: Swarm expected position asymptotically converges to the non-dominated attractor vector $p$: $\mathbb{E}[q_s] \to p$ as $s \to \infty$.
- **Lemma 2 (Second-Order Variance Convergence)**: Particle position variance strictly vanishes: $\text{Var}[q_s] \to 0$ as $s \to \infty$.
