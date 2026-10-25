# On the Limitations of Multi-Objective Neuro-Evolutionary Traffic Classification in SDWNs: A Negative Result and Lessons Learned

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.example.svg)](https://doi.org/10.5281/zenodo.example)

This repository contains the complete empirical reproduction suite and publication package for the research paper:
> **"On the Limitations of Multi-Objective Neuro-Evolutionary Traffic Classification in SDWNs: A Negative Result and Lessons Learned"**  
> *Target Submission*: Q2 Journal Submission (Merged Senior & Team Research)

---

## 📌 Summary: The Empirical Negative Result

This work investigates whether a lightweight, multi-objective Particle Swarm Optimization (MOPSO)-trained Feed-Forward Neural Network (FFNN, 325 parameters) can produce a viable edge-deployable traffic classifier for Software-Defined Wireless Networks (SDWNs).

When evaluated on real-world packet traces (**ISCX VPN 2016** and **USTC-TFC 2016**), our findings show that **MOPSO-FFNN-AD is strictly Pareto-dominated** by modern deep learning baselines across both accuracy and composite physical overhead:

| Method | Parameters ($D$) | USTC Acc (Time-Blocked) | ISCX Acc (Time-Blocked) | USTC Overhead $F$ | ISCX Overhead $F$ | Multi-Objective Status |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **Compact Transformer** | 18,437 | $77.20 \pm 4.24\%$ | $53.37 \pm 6.60\%$ | **$0.1738$** | **$0.3239$** | Strictly Pareto-dominates |
| **PyTorch LSTM** | 13,093 | **$78.17 \pm 4.46\%$** | **$57.30 \pm 9.25\%$** | $0.2007$ | $0.3343$ | Strictly Pareto-dominates |
| **PyTorch 1D-CNN** | 2,373 | $77.40 \pm 3.85\%$ | $53.20 \pm 9.02\%$ | $0.1989$ | $0.3395$ | Strictly Pareto-dominates |
| **PSO-FFNN (Base [A])** | 325 | $71.73 \pm 3.14\%$ | $41.27 \pm 8.43\%$ | $0.3559$ | $0.4792$ | Pradhan et al. (IET 2022) |
| **MOPSO-FFNN-AD (Ours)**| **325** | **$66.60 \pm 9.56\%$** | **$38.23 \pm 8.30\%$** | **$0.3742$** | **$0.4837$** | **Pareto-Dominated (Negative Result)** |

### Key Post-Mortem Insights:
1. **Flawed Overhead Proxies**: Weight-magnitude thresholds ($|w| > 0.3, |w| > 0.05$) fail because modern deep learning regularized via batch norm and weight decay naturally yields small weights, resulting in lower $F$ scores than unregularized FFNNs despite having $56\times$ more parameters.
2. **Representational Bottleneck**: A 325-parameter network ($8 \to 16 \to 8 \to 5$) lacks capacity for encrypted traffic distributions ($38.2\%$ on ISCX VPN).
3. **Temporal Leakage**: Standard random cross-validation overstates accuracy by $7\% - 9\%$ due to temporal autocorrelation within network bursts. Time-based blocking CV eliminates this leakage.
4. **Feature Vulnerabilities**: `dst_port` provides zero utility under port 443 HTTPS multiplexing; `ttl` is an unreliable topology artifact that collapses under noise.

---

## 🚀 Quickstart & Reproduction Guide

### 1. Environment Setup (Using `uv`)
```bash
# Clone the repository
git clone https://github.com/rikkumahan/CN_research.git
cd CN_research

# Create virtual environment and install pinned dependencies
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Verify Automated Unit Tests (13/13 Passing)
```bash
uv run pytest -v
```

### 3. Reproduce Time-Based Blocking Cross-Validation (Step 3)
```bash
uv run python src/run_time_blocked_cv.py
```
Outputs:
- `results/table2_time_blocked_cv_iscx.csv`
- `results/table2_time_blocked_cv_ustc.csv`
- `figures/fig_time_blocked_cv_accuracy_iscx.png`
- `figures/fig_time_blocked_cv_accuracy_ustc.png`

### 4. Reproduce Feature Robustness Experiments (Step 4)
```bash
uv run python src/feature_robustness_experiments.py
```
Outputs:
- TTL Perturbation: `results/ttl_robustness_results_ustc.csv` & `figures/fig_ttl_corruption_robustness_ustc.png`
- Destination Port Ablation: `results/dst_port_ablation_iscx.csv`
- Higher-Order IAT Moments: `results/feature_importance_with_iat_moments_iscx.csv` & `figures/fig_feature_importance_moments_iscx.png`
- Feature Count Diminishing Returns: `results/diminishing_returns_feature_count_iscx.csv` & `figures/fig_feature_diminishing_returns_iscx.png`

### 5. Reproduce SOTA Comparison (Step 2)
```bash
# Generates updated Table 6 SOTA comparison table
cat results/table6_sota_comparison.csv
```

---

## 📁 Repository Structure

```
CN_research/
├── data/
│   ├── raw/                 # Input PCAP files
│   ├── processed/           # Extracted 8-feature flows (iscx_flows.csv, ustc_flows.csv)
│   └── metadata/            # Dataset duration statistics and label mappings
├── src/
│   ├── dataset_loader.py    # PCAP streaming feature extractor
│   ├── models.py            # FFNN, 1D-CNN, LSTM, Transformer & composite fitness F
│   ├── mopso_optimizer.py   # Multi-objective PSO & Page-Hinkley drift detector
│   ├── run_experiments.py   # Standard 10-fold CV, policy ablation, permutation importance
│   ├── run_time_blocked_cv.py # Time-based blocking cross-validation (Step 3)
│   └── feature_robustness_experiments.py # TTL noise, dst_port ablation, IAT moments (Step 4)
├── docs/
│   ├── RESEARCH_PAPER_FULL_MANUSCRIPT.md # Complete Q2 journal manuscript
│   ├── PRESENTATION_VTOP_SLIDES.md       # Final Review 3 presentation slide deck
│   └── PAPER_SECTION_UPDATES.md          # Revision log and mathematical proofs
├── figures/                 # Publication-grade figures (boxplots, decay curves, Pareto fronts)
├── results/                 # Raw and summary CSV experiment outputs
├── tests/                   # 13 automated unit tests
├── requirements.txt         # Pinned dependency specifications
└── Dockerfile               # Containerized reproduction environment
```

---

## 🐳 Docker Reproduction

To reproduce all results in a completely isolated Docker container:
```bash
docker build -t cn-research .
docker run --rm -v $(pwd)/results:/app/results cn-research
```

---

## 📜 Archival & Zenodo DOI Instructions

To obtain a persistent DOI for journal submission:
1. Link the GitHub repository [https://github.com/rikkumahan/CN_research.git](https://github.com/rikkumahan/CN_research.git) to [Zenodo](https://zenodo.org/).
2. Create a GitHub Release tagged `v3.0.0-review3-final`.
3. Zenodo will mint an archival DOI (e.g., `10.5281/zenodo.XXXXXXX`) that can be cited in the manuscript.

---

## ⚖️ License & Ethical Standards
This software is licensed under the MIT License. Evaluation strictly preserves packet header metadata without inspecting or decrypting payload content, maintaining full compliance with GDPR and user privacy regulations.
