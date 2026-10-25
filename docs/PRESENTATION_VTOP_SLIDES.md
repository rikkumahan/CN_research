# Final Review 3 Presentation Slide Deck (Q2 Journal Defense)

> **Paper Title**: On the Limitations of Multi-Objective Neuro-Evolutionary Traffic Classification in SDWNs: A Negative Result and Lessons Learned  
> **Target Venue**: Q2 Journal Submission (Merged Senior & Team Work)  
> **Review**: Final Review 3 / Publication Defense  
> **Framing**: Rigorous Negative Result & Empirical Post-Mortem

---

## Slide 1: Title & Project Overview

### 📌 Slide Content:
- **Project Title**: On the Limitations of Multi-Objective Neuro-Evolutionary Traffic Classification in SDWNs: A Negative Result and Lessons Learned
- **Core Investigation**: Can lightweight multi-objective neuro-evolutionary optimization (MOPSO-FFNN-AD) produce an edge-deployable traffic classifier that rivals deep learning?
- **Key Empirical Discovery (Review 3)**:
  - When evaluated on **real-world PCAP benchmarks** (ISCX VPN 2016 & USTC-TFC 2016), the proposed MOPSO-FFNN-AD is **strictly Pareto-dominated** by all deep learning baselines across both accuracy AND composite overhead $F$.
  - Rather than making indefensible "trade-off" claims, we provide an honest, rigorous **Negative Result paper** analyzing the architectural and metric root causes.
- **Publication Target**: Q2 Journal Submission (IEEE Access / IET Communications / Elsevier Computer Networks).

### 🗣️ Speaker Script:
> *"Respected professors, welcome to our Final Review 3 presentation. In this review, we merge our senior's foundation with our real-world evaluations for a Q2 journal submission. Our central finding is an honest, rigorous negative result: when tested on real encrypted PCAPs, the proposed MOPSO-FFNN-AD is strictly Pareto-dominated by deep learning baselines on both accuracy and overhead. Today, we present why this happened, why proxy overhead metrics fail, and what lessons networking researchers must learn."*

---

## Slide 2: The Core Problem — Pareto Domination on Real Benchmarks

### 📌 Slide Content (Table for PPT):
| Method | USTC Accuracy ($\uparrow$) | ISCX Accuracy ($\uparrow$) | USTC Overhead $F$ ($\downarrow$) | ISCX Overhead $F$ ($\downarrow$) | Trainable Parameters |
|:---|:---:|:---:|:---:|:---:|:---:|
| **MOPSO-FFNN-AD (Proposed)** | **$62.97\%$** | **$37.87\%$** | **$0.3816$** | **$0.4817$** | **325** |
| **1D-CNN Baseline** | $77.60\%$ | $61.50\%$ | $0.1997$ | $0.3064$ | 2,373 |
| **LSTM Baseline** | $77.47\%$ | $64.23\%$ | $0.2008$ | $0.3067$ | 13,093 |
| **Transformer Baseline** | **$78.57\%$** | **$62.13\%$** | **$0.1686$** | **$0.2937$** | 18,437 |
| **PSO-FFNN (Base Paper A)** | $74.90\%$ | $47.93\%$ | $0.3544$ | $0.4486$ | 325 |

- **What is Pareto Domination?**
  - A method is Pareto-dominated when an alternative achieves **higher accuracy AND lower overhead simultaneously**.
  - Transformer ($78.57\%$, $F=0.1686$) strictly beats MOPSO ($62.97\%$, $F=0.3816$) on **every single axis**.
  - **Scientific Conclusion**: This cannot be defended as an "intentional compromise." It is an empirical limitation.

### 🗣️ Speaker Script:
> *"This table summarizes the core dilemma. In multi-objective optimization, a compromise means winning on one axis while losing on another. But here, the Transformer achieves 78.6% accuracy with an overhead of 0.1686, while MOPSO achieves only 63.0% accuracy with an overhead of 0.3816. The proposed method loses on both axes simultaneously. In multi-objective terms, it is strictly Pareto-dominated."*

---

## Slide 3: Root Cause 1 — Misaligned Overhead Metrics ($F$)

### 📌 Slide Content:
- **How Composite Overhead $F$ Was Defined**:
  $$F = 0.45(1 - \text{Acc}) + 0.20 f_{\text{FRUR}} + 0.15 f_{\text{CPU}} + 0.10 f_{\text{FSD}} + 0.10 f_{\text{BW}}$$
  where $f_{\text{CPU}} = \frac{1}{D}\sum \mathbb{I}(|w| > 0.3)$ and $f_{\text{BW}} = \frac{1}{D}\sum \mathbb{I}(|w| > 0.05)$.
- **Why Deep Learning Cheated the Proxy Metric**:
  1. Modern DL layers use **Batch Normalization** and **Xavier/Kaiming initialization** ($\sigma \approx 0.1 - 0.2$).
  2. DL trains with **$L_2$ weight decay** (`weight_decay=1e-4`), which continuously shrinks weights toward zero.
  3. Consequently, DL weights naturally stay below $0.30$, yielding low $f_{\text{CPU}}$ and $f_{\text{BW}}$ without any multi-objective pressure!
- **Why FFNN was Penalized**:
  - The 325-parameter FFNN was trained with unconstrained swarm search without weight decay. Individual weights ranged between $[-3.0, +3.0]$, artificially driving up $F$.
- **The Paradox**: An 18,437-parameter Transformer achieved a lower "overhead" score than a 325-parameter network!

### 🗣️ Speaker Script:
> *"Why did this happen? Root Cause 1 is that the overhead formula is a broken proxy for hardware cost. Terms f3, f4, and f5 penalize weights exceeding 0.30. Deep learning models use weight decay and batch normalization, keeping weights small by design. Particle swarm optimization does not use weight decay. So the formula penalized the 325-parameter FFNN while giving the 18,000-parameter Transformer a clean score. Weight magnitude is not hardware cost."*

---

## Slide 4: Root Cause 2 & 3 — Representational Bottleneck & Feature Flaws

### 📌 Slide Content:
- **Root Cause 2: 325-Parameter Network Capacity Bottleneck**:
  - Encrypted traffic classification requires learning subtle non-linear distributions from high-entropy packet streams.
  - A tiny network ($8 \to 16 \to 8 \to 5$, $D=325$) lacks the mathematical **representational capacity** for encrypted flow separation ($37.87\%$ on ISCX).
- **Root Cause 3: Feature Vulnerabilities**:
  - **`dst_port` Collapses to Zero Importance**: Ranked dead last ($\Delta F \approx -0.00007$) because web chat, streaming, and malware all multiplex over **port 443 (HTTPS/TLS)** to evade firewalls.
  - **`ttl` is an Unreliable Artifact**: Ranked #1 on USTC malware, but TTL only reflects the testbed hop distance. In production, TTL is easily spoofed or altered by intermediate routers.
  - **Missing Statistical Moments**: The 8 features lacked higher-order moments (IAT variance, skewness, kurtosis) necessary to capture burstiness.

### 🗣️ Speaker Script:
> *"Root Causes 2 and 3 concern network capacity and features. A 325-parameter neural network cannot learn the complex manifolds of encrypted VPN flows. Furthermore, our permutation feature analysis revealed that destination port contributes zero signal because everything tunnels over port 443. And while TTL ranked first on malware, TTL is a fragile artifact of network topology that cannot be relied upon in real deployments."*

---

## Slide 5: Comprehensive State-of-the-Art (SOTA) Comparison

### 📌 Slide Content (Table 6 for PPT):
| Method | Architecture / Category | Parameters | USTC Accuracy | ISCX Accuracy | Priority / Status |
|:---|:---|:---:|:---:|:---:|:---|
| **ET-BERT (Lin et al. 2022)** | Pre-trained Contextual Transformer | $\approx 50\text{M}$ | $96.95\%$ | — | Published SOTA (Must cite) |
| **YaTC (Chen et al. 2023)** | Large Traffic Transformer | $\approx 30\text{M}$ | $97.86\%$ | — | Published SOTA (Must cite) |
| **FS-Net (Liu et al. 2019)** | End-to-End Bi-RNN Payload Model | $\approx 10\text{M}$ | $87.05\%$ | $52.03\%$ | Published SOTA (Must cite) |
| **FlowPic (Shapira 2021)** | 2D Flow Image Visual CNN | $\approx 2\text{M}$ | $> 90.0\%$ | $> 85.0\%$ | Published SOTA (Must cite) |
| **TFE-GNN (Shen 2023)** | Traffic Flow Graph Neural Network | $\approx 5\text{M}$ | $97.47\%$ | $91.92\%$ | Published SOTA (Must cite) |
| **Transformer (Ours)** | Generic Compact Transformer | $18,437$ | $78.57\%$ | $62.13\%$ | Re-implemented baseline |
| **LSTM (Ours)** | Generic 2-Layer LSTM | $13,093$ | $77.47\%$ | $64.23\%$ | Re-implemented baseline |
| **1D-CNN (Ours)** | Generic 2-Layer 1D-CNN | $2,373$ | $77.60\%$ | $61.50\%$ | Re-implemented baseline |
| **MOPSO-FFNN-AD (Ours)** | Multi-Objective Swarm + FFNN | **325** | **$62.97\%$** | **$37.87\%$** | Proposed (Pareto-dominated) |

### 🗣️ Speaker Script:
> *"In Table 6, we benchmark our framework against both our re-implemented generic DL baselines and published SOTA literature. Published SOTA models like ET-BERT and YaTC reach 97% to 98% accuracy by using tens of millions of parameters. Even our un-tuned 18,000-parameter Transformer reaches 78.6%. This contextualizes our paper: even SOTA struggles with edge switch constraints, but tiny neuro-evolutionary models do not provide the answer."*

---

## Slide 6: Eliminating Temporal Leakage — Time-Based Blocking Cross-Validation

### 📌 Slide Content:
- **The Methodological Pitfall: Random Cross-Validation**:
  - In network traffic, packets belonging to the same flow or session share strong temporal autocorrelation.
  - Standard random 10-fold CV randomly assigns flows from the same burst into train and test folds, artificially inflating test accuracy.
- **The Rigorous Fix: Time-Based Blocking CV**:
  1. Sort all captured flows strictly by timestamps.
  2. Divide flows into 10 contiguous chronological time blocks ($B_1, B_2, \dots, B_{10}$).
  3. Sequentially train on 9 blocks and evaluate on the 10th block.
- **Outcome**: While accuracy drops slightly, the evaluation is 100% leak-free and reflects true operational performance.

### 🗣️ Speaker Script:
> *"A critical methodological improvement for Review 3 is eliminating temporal leakage. Standard cross-validation randomly shuffles flows, allowing flows from the same user session or attack burst to appear in both training and test sets. We replaced this with strict Time-Based Blocking Cross-Validation: sorting traffic chronologically into 10 contiguous blocks. This provides an honest, leak-free benchmark."*

---

## Slide 7: Feature Robustness Analysis (TTL & IAT Moments)

### 📌 Slide Content:
- **Experiment 1: TTL Corruption Sensitivity**:
  - We injected bounded noise into the `ttl` feature: $\text{TTL}' = \text{clip}(\text{TTL} + \mathcal{U}(-15, 15), 1, 255)$.
  - Result: Classification accuracy collapses, proving `ttl` is an unreliable, fragile feature that will fail in dynamic networks.
- **Experiment 2: Higher-Order IAT Moments**:
  - Extended flow extraction beyond mean IAT to include **variance, skewness, and kurtosis**.
  - Permutation importance shows higher-order moments provide genuine physical discrimination between interactive chat and streaming bursts.
- **Experiment 3: Omission of `dst_port`**:
  - Removing `dst_port` produces zero accuracy degradation, confirming that port numbers are obsolete under HTTPS/TLS 1.3 multiplexing.

### 🗣️ Speaker Script:
> *"To complete our feature post-mortem, we conducted three targeted experiments. When we added noise to TTL, accuracy collapsed, proving the model was over-reliant on a topology-dependent artifact. Destination port contributed nothing due to port 443 multiplexing. On the other hand, adding higher-order IAT moments—variance and skewness—captures genuine packet burstiness without inspecting encrypted payloads."*

---

## Slide 8: Reframing Stability Proofs — Math vs. Classification Performance

### 📌 Slide Content:
- **Lemmas 1 & 2 Moved to Appendix A**:
  - **Lemma 1**: Characteristic spectral radius $\rho = 0.8543 < 1.0 \implies \mathbb{E}[q_s] \to p$ (First-order mean convergence).
  - **Lemma 2**: Safety margin $+0.355 \implies \text{Var}[q_s] \to 0$ (Second-order variance convergence).
- **The Vital Scientific Distinction**:
  - Lemmas 1 & 2 prove that the **swarm optimizer is mathematically stable** (particles will not diverge or explode).
  - However, **swarm stability does not imply classifier accuracy**.
  - A stable swarm converging smoothly to a local minimum inside a low-capacity 325-parameter space still produces an ineffective classifier!
- **Paper Framing**: We honestly separate optimization convergence from downstream task efficacy.

### 🗣️ Speaker Script:
> *"Our paper contains two formal mathematical proofs: Lemma 1 proving first-order expectation convergence, and Lemma 2 proving second-order variance stability. Following our supervisor's guidance, we moved these proofs to Appendix A. We explicitly explain in the text that mathematical stability proves the swarm does not explode, but stability does not guarantee classification accuracy. A stable swarm converging to an inadequate architecture is still inadequate."*

---

## Slide 9: Review 3 Deliverables & Q2 Journal Submission Package

### 📌 Slide Content:
- **1. Manuscript Fully Reframed**:
  - New Title: *"On the Limitations of Multi-Objective Neuro-Evolutionary Traffic Classification in SDWNs: A Negative Result and Lessons Learned"*
  - Honest abstract, introduction, and post-mortem discussion.
- **2. Empirical Rigor & Codebase**:
  - Time-based blocking cross-validation implemented.
  - Real SOTA baselines integrated into Table 6 (ET-BERT, YaTC, FS-Net, FlowPic).
  - TTL robustness & IAT moment experiments completed.
  - Fully passing unit test suite (**13/13 passing**).
- **3. Archival & Reproducibility**:
  - Public GitHub repository with reproduction instructions.
  - Pinned `requirements.txt` and Zenodo DOI archiving ready.

### 🗣️ Speaker Script:
> *"In summary, we have completely transformed this manuscript from an indefensible 'compromise' paper into a rigorous, highly publishable Negative Result and Lessons Learned contribution for a Q2 journal. We have eliminated misleading claims, added real SOTA comparisons, resolved temporal leakage, ablated fragile features, and packaged all code with full unit test verification. Thank you, and we welcome your feedback."*

---
