# Results & Benchmarks Guide — Review 3 (Negative Result Reframing)

This directory contains the **publication-grade benchmark figures (300 DPI)** summarizing our empirical findings and research achievements for Review 3. Each figure is designed to tell a clear, defensible scientific story during faculty reviews, presentations, and viva defenses.

---

## 🖼️ Visual Benchmark Index

| File | Figure Title | Core Takeaway to Tell Faculty |
| :--- | :--- | :--- |
| **[`01_core_finding_pareto_domination.png`](file:///Users/akshaykumarpudi/Desktop/CN_research/results_review3/01_core_finding_pareto_domination.png)** | The Core Negative Result: Pareto Domination | Deep learning baselines strictly dominate MOPSO-FFNN-AD on **both** accuracy and overhead $F$. It is not a trade-off; it is a clear empirical negative result. |
| **[`02_synthetic_illusion_vs_real_pcap.png`](file:///Users/akshaykumarpudi/Desktop/CN_research/results_review3/02_synthetic_illusion_vs_real_pcap.png)** | The "Synthetic Illusion" vs. Real PCAPs | The senior’s 94.3% claim worked only on artificial Gaussian clusters; on real encrypted PCAPs, MOPSO collapses to 37.8%. |
| **[`03_sota_benchmarks_and_edge_constraints.png`](file:///Users/akshaykumarpudi/Desktop/CN_research/results_review3/03_sota_benchmarks_and_edge_constraints.png)** | SOTA Classifiers vs. Edge Hardware Limits | Published SOTA (ET-BERT, YaTC) reaches 97%+ but needs GPU servers (>10M params). Our work evaluates the boundary of edge switch TCAM (<10K params). |
| **[`04_temporal_leakage_random_vs_time_blocked_cv.png`](file:///Users/akshaykumarpudi/Desktop/CN_research/results_review3/04_temporal_leakage_random_vs_time_blocked_cv.png)** | Temporal Autocorrelation Leakage Exposed | Random CV artificially inflates accuracy by leaking temporal session patterns. Time-blocked CV eliminates leakage, and Pareto domination still holds. |
| **[`05_ttl_perturbation_fragility.png`](file:///Users/akshaykumarpudi/Desktop/CN_research/results_review3/05_ttl_perturbation_fragility.png)** | Feature Fragility: TTL Noise Collapse | TTL is a fragile network topology artifact (hop count). When corrupted by realistic network jitter, classifier accuracy collapses by 30.5%. |
| **[`06_feature_importance_and_iat_moments.png`](file:///Users/akshaykumarpudi/Desktop/CN_research/results_review3/06_feature_importance_and_iat_moments.png)** | Feature Post-Mortem & Higher-Order IAT Moments | `dst_port` has near-zero utility due to HTTPS port 443 multiplexing. Higher-order IAT skewness and variance capture true encrypted traffic burstiness. |
| **[`07_diminishing_returns_feature_saturation.png`](file:///Users/akshaykumarpudi/Desktop/CN_research/results_review3/07_diminishing_returns_feature_saturation.png)** | Feature Space Saturation (Diminishing Returns) | Accuracy plateaus after 5 features, justifying our compact 8-feature schema for edge switch memory constraints. |
| **[`08_swarm_stability_vs_classifier_accuracy.png`](file:///Users/akshaykumarpudi/Desktop/CN_research/results_review3/08_swarm_stability_vs_classifier_accuracy.png)** | Swarm Mathematical Stability $\neq$ Generalization | Proves Lemmas 1 & 2 mathematically hold ($\rho = 0.8543 < 1.0$), but numerical swarm convergence simply traps the 325-param model in a sub-optimal local basin. |

---

## 🔍 Detailed Slide-by-Slide Explanation Scripts

### Figure 1: `01_core_finding_pareto_domination.png`
- **What it shows**: A bi-objective scatter plot showing Classification Accuracy (%) on the Y-axis and Composite Physical Overhead $F$ on the X-axis for both USTC-TFC and ISCX VPN benchmarks.
- **Key Metrics**:
  - USTC: Proposed MOPSO ($62.97\%$, $F=0.3816$) vs. Transformer ($78.57\%$, $F=0.1686$) and LSTM ($77.47\%$, $F=0.2008$).
  - ISCX: Proposed MOPSO ($37.87\%$, $F=0.4817$) vs. LSTM ($64.23\%$, $F=0.3067$) and Transformer ($62.13\%$, $F=0.2937$).
- **Viva Defense Script**:
  > *"Mam/Sir, this figure illustrates the primary empirical finding of our study. In multi-objective optimization, a valid trade-off requires a method to win on at least one objective. Here, deep learning baselines occupy the top-left ideal Pareto region—achieving higher accuracy AND lower overhead $F$ simultaneously. This proves MOPSO-FFNN-AD is strictly Pareto-dominated, justifying our reframing as a negative result."*

---

### Figure 2: `02_synthetic_illusion_vs_real_pcap.png`
- **What it shows**: Grouped bar chart comparing the senior's synthetic dataset claim against real-world PCAPs.
- **Key Metrics**:
  - Synthetic Gaussian data: $94.33\%$ accuracy.
  - Real USTC PCAP: $62.97\%$ ($-31.4\%$ drop).
  - Real ISCX Encrypted PCAP: $37.87\%$ ($-56.5\%$ collapse).
- **Viva Defense Script**:
  > *"Prior work reported 94.33% because it was tested on idealized synthetic Gaussian data. When we stream real packet captures (PCAPs) from ISCX and USTC, the evolutionary FFNN collapses. Meanwhile, gradient-trained deep learning models remain resilient at 62%–78%."*

---

### Figure 3: `03_sota_benchmarks_and_edge_constraints.png`
- **What it shows**: Classification accuracy plotted against parameter count $D$ on a logarithmic scale from 100 to 100 million parameters.
- **Key Highlights**:
  - Published SOTA (ET-BERT, YaTC, TFE-GNN) achieves $96\%–98\%$ accuracy but requires $5\text{M}–50\text{M}$ parameters (server/GPU only).
  - OpenFlow SDWN switches have strict TCAM/SRAM budgets ($<10,000$ parameters).
- **Viva Defense Script**:
  > *"Published state-of-the-art models like ET-BERT achieve over 97% accuracy, but they require 50 million parameters and server GPUs. In SDWN edge switches, TCAM budgets limit models to under 10,000 parameters. Our work tests whether evolutionary models can fill this edge niche, proving that 325 parameters is insufficient for encrypted traffic manifolds."*

---

### Figure 4: `04_temporal_leakage_random_vs_time_blocked_cv.png`
- **What it shows**: Comparison between conventional Random 10-Fold CV and chronological Time-Based Blocking CV.
- **Key Metrics**:
  - Random CV inflates accuracy by $6\%–8\%$ because flows from the same session appear in both training and test folds.
  - In Time-Blocked CV, even after eliminating temporal leakage, deep learning models still outperform MOPSO by $+15\%$ to $+19\%$.
- **Viva Defense Script**:
  > *"Standard random cross-validation leaks temporal patterns because packets from the same flow occur close in time. We built a time-blocked CV pipeline splitting data chronologically. This lowers accuracy across all models to realistic levels, proving that our negative result is not an artifact of data leakage."*

---

### Figure 5: `05_ttl_perturbation_fragility.png`
- **What it shows**: Accuracy decay of FFNN and 1D-CNN as artificial TTL jitter and randomization are injected.
- **Key Metrics**:
  - Under realistic TTL jitter (noise = 150), FFNN accuracy collapses from $78.7\%$ down to $48.2\%$ (a $30.5\%$ loss).
- **Viva Defense Script**:
  > *"Prior papers ranked TTL as the most important feature. However, our perturbation experiment proves that TTL is merely a topology artifact reflecting router hop counts, not application behavior. Corrupting TTL degrades accuracy by over 30%, showing why relying on unverified features in SDN is dangerous."*

---

### Figure 6: `06_feature_importance_and_iat_moments.png`
- **What it shows**: Permutation feature importance comparing the standard 8 features against higher-order statistical IAT moments.
- **Key Findings**:
  - `dst_port` has near-zero utility ($\Delta F \approx -0.00007$) in modern traffic because virtually all web traffic tunnels over TLS port 443.
  - `iat_skewness` ($10.6\%$) and `iat_variance` ($6.3\%$) provide significant discriminative power by capturing burstiness.
- **Viva Defense Script**:
  > *"In modern encrypted networks, destination port is useless because everything uses port 443. Instead, our experiments show that higher-order moments like IAT skewness and variance capture the true burstiness of encrypted sessions."*

---

### Figure 7: `07_diminishing_returns_feature_saturation.png`
- **What it shows**: Accuracy vs. number of features, showing performance saturation beyond 5 features alongside parameter growth.
- **Key Finding**: Accuracy plateaus between 5 and 8 features, confirming that extracting more than 8 features wastes memory without providing accuracy gains.
- **Viva Defense Script**:
  > *"This curve justifies why our feature vector contains exactly 8 features. Accuracy saturates after 5 features, so adding additional flow headers increases switch memory consumption without improving classification."*

---

### Figure 8: `08_swarm_stability_vs_classifier_accuracy.png`
- **What it shows**: Eigenvalue distribution of the swarm transition matrix inside the unit circle ($\rho = 0.8543 < 1.0$), contrasted with the classifier accuracy trajectory trapped in a local minimum.
- **Key Proof**:
  - Lemma 1 proves first-order swarm convergence ($\rho < 1.0$).
  - Lemma 2 proves variance stability (positive margin $+0.3550$).
- **Viva Defense Script**:
  > *"The senior paper emphasized mathematical stability proofs (Lemmas 1 and 2). We mathematically verified these proofs—the spectral radius is indeed 0.8543, which is strictly less than 1.0. However, our key scientific insight is that mathematical swarm convergence does not imply classifier accuracy; the swarm stably converges into a sub-optimal local minimum."*
