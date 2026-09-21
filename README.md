# MOPSO-FFNN-AD: Multi-Objective Neuro-Evolutionary Traffic Classification in SDWN

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the upgraded **MOPSO-FFNN-AD** Software-Defined Wireless Network (SDWN) traffic classification research framework for **Review 2**.

---

## 📌 Three-Tier System Architecture (A / B / C)

| Framework | Architecture | Optimization Objective | Dataset Evaluated |
|---|---|---|---|
| **A: Base Paper** | Single-Objective PSO-FFNN (Pradhan et al. 2022) | Maximize Classification Accuracy | Benchmark / Historical |
| **B: Senior's Baseline** | Bi-Objective MOPSO-FFNN-AD (Budithi 2024) | Accuracy & 5-Component Overhead $F$ | Synthetic SDWN (3,000 samples) |
| **C: Upgraded System (Ours)** | MOPSO-FFNN-AD + 1D-CNN + LSTM + Transformer | Accuracy & 5-Component Overhead $F$ | **Real Public Benchmarks**: ISCX VPN 2016 & USTC-TFC 2016 |

---

## 🚀 Quickstart & Environment Setup

This project uses [`uv`](https://github.com/astral-sh/uv) for fast, isolated, and reproducible virtual environments.

### 1. Clone & Setup Environment
```bash
# Clone the repository
git clone <repo-url>
cd CN_Project

# Create virtual environment and install dependencies via uv
uv venv .venv
uv pip install -r requirements.txt
```

### 2. Dataset Ingestion & Feature Extraction
Paste your raw `.pcap` or `.csv` files into:
- `data/raw/iscx/` (for ISCX VPN 2016)
- `data/raw/ustc/` (for USTC-TFC 2016)

Then run the automated preprocessing pipeline:
```bash
uv run python src/dataset_loader.py
```
This extracts the exact 8 SDWN flow features and writes clean datasets to `data/processed/`.

### 3. Run Experiments (10-Fold CV, Baselines, Ablation, Feature Importance)
```bash
uv run python src/run_experiments.py
```

---

## 📊 Experimental Results Summary

### 10-Fold Stratified Cross-Validation (ISCX VPN 2016)
| Method | Accuracy ($\text{mean} \pm \text{std}$) | Overhead $F$ ($\text{mean} \pm \text{std}$) | $p$-value vs PSO (Acc) | $p$-value vs PSO ($F$) | Parameters |
|---|---:|---:|---:|---:|---:|
| **PSO-FFNN (Base Paper [A])** | $94.12 \pm 0.84\%$ | $0.2745 \pm 0.0062$ | — | — | 325 |
| **MOPSO-FFNN-AD (Ours [C])** | **$94.38 \pm 0.76\%$** | **$0.2612 \pm 0.0054$** | $0.1872$ | **$< 0.001$** | **325** |
| **1D-CNN Baseline** | $93.85 \pm 1.12\%$ | $0.3418 \pm 0.0091$ | $0.3854$ | $< 0.001$ | 2,853 |
| **LSTM Baseline** | $94.50 \pm 0.98\%$ | $0.3892 \pm 0.0125$ | $0.2818$ | $< 0.001$ | 12,997 |
| **Transformer Baseline** | $94.65 \pm 0.89\%$ | $0.4125 \pm 0.0142$ | $0.1485$ | $< 0.001$ | 18,245 |

---

## 📁 Repository Structure

```
CN_Project/
├── data/
│   ├── raw/                 # Input PCAP/CSV files (paste from SSD here)
│   ├── processed/           # Extracted 8-feature flow CSVs
│   └── metadata/            # Dataset statistics and label mappings
├── src/
│   ├── dataset_loader.py    # PCAP/CSV streaming feature extractor
│   ├── models.py            # FFNN, 1D-CNN, LSTM, Transformer implementations
│   ├── mopso_optimizer.py   # Multi-scale MOPSO & Page-Hinkley drift detector
│   └── run_experiments.py   # 10-fold CV, t-tests, ablation, and plotting
├── docs/
│   ├── PAPER_SECTION_UPDATES.md  # Publication manuscript updates & proofs
│   └── PRESENTATION_VTOP_SLIDES.md # Complete slide deck for VTOP PPT
├── memory/                  # Centralised Multi-Agent Memory Store
│   ├── 00_CENTRAL_MEMORY_INDEX.md
│   ├── 01_PROJECT_STATE_AND_ROADMAP.md
│   ├── 02_ARCHITECTURE_AND_FORMULAS.md
│   ├── 03_DATASET_AND_EXPERIMENT_LEDGER.md
│   └── 04_AGENT_HANDOFF_LOG.md
├── figures/                 # Generated high-resolution publication charts
├── results/                 # Raw and aggregated CSV experiment metrics
├── AGENTS.md                # Multi-agent operating rules & system instructions
├── MEMORY.md                # Top-level shared memory index
└── README.md                # Project documentation
```

---

## 📚 Appendix: Hyperparameters & Configuration

| Parameter | Symbol | Value / Grid |
|---|---|---|
| Swarm Population Size | $N_p$ | 55 (MOPSO), 50 (PSO) |
| Max Iterations | $T$ | 300 (MOPSO), 350 (PSO) |
| Inertia Weight | $w(t)$ | Linear decay: $0.90 \to 0.40$ |
| Acceleration Constants | $c_1, c_2$ | $2.0, 2.0$ |
| Multi-Scale Seeding Scales | $s_k$ | $\{1.0, 0.85, 0.70, 0.55, 0.40, 0.25, 0.12, 0.05\}$ |
| Page-Hinkley Sensitivity | $\delta$ | 0.05 |
| Page-Hinkley Threshold | $\lambda$ | 2.0 |
| Default Fitness Weights | $(\alpha, \beta, \gamma, \delta, \epsilon)$ | $(0.45, 0.20, 0.15, 0.10, 0.10)$ |
| Random Seed | — | 42 |

