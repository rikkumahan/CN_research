# 01. Project State & Roadmap

## Current Status: Phase 5 (Review 3 / Q2 Journal Negative Result Transformation) Completed

### 📌 Milestone Checklist

- [x] **Phase 0 — Setup & Environment**
  - [x] Virtual environment `.venv` created via `uv` (Python 3.12)
  - [x] Dependencies installed (`torch`, `scikit-learn`, `pandas`, `numpy`, `scipy`, `matplotlib`, `pypdf`, `scapy`, `requests`, `pytest`)
  - [x] Senior PDF (`budithi.pdf`) text extracted (`budithi_extracted.txt`)
  - [x] Centralised memory store created (`MEMORY.md` & `memory/`)
  - [x] Multi-agent instructions created (`AGENTS.md`)

- [x] **Phase 1 — Data Pipeline (`src/dataset_loader.py`)**
  - [x] Ingestion and PCAP streaming flow extraction pipeline built for:
    1. ISCX VPN 2016
    2. USTC-TFC 2016
  - [x] Standard 8-feature schema extractor implemented
  - [x] Strict leakage prevention: standard scaling fit strictly on training splits.

- [x] **Phase 2 — Core Models & Optimizer (`src/models.py`, `src/mopso_optimizer.py`)**
  - [x] Base Paper PSO-FFNN (A) implemented
  - [x] Senior's MOPSO-FFNN-AD with Page-Hinkley drift detector (B & C) implemented
  - [x] Deep Learning Baselines (C) implemented: 1D-CNN, LSTM, Compact Transformer
  - [x] Centralized 5-component fitness calculation $F$

- [x] **Phase 3 — Review 2 Experiments (`src/run_experiments.py`)**
  - [x] 10-fold Stratified Cross-Validation runner
  - [x] Statistical paired t-tests (MOPSO-FFNN-AD vs PSO-FFNN)
  - [x] 3-policy ablation study ($\alpha=0.8, \epsilon=0.5, \delta=0.5$)
  - [x] Permutation feature importance on all 8 features
  - [x] Review 2 publication figures

- [x] **Phase 4 — Review 2 Paper & Presentation Assets**
  - [x] Full manuscript, DOCX document, slides, and guides

- [x] **Phase 5 — Final Review 3 & Q2 Journal Transformation (The Negative Result Reframing)**
  - [x] **Step 1: Scrub Misleading Claims**: Removed all false "intentional compromise/trade-off" claims; framed Pareto domination honestly across manuscript, updates, and slides.
  - [x] **Step 2: Add Real SOTA Baselines**: Updated `results/table6_sota_comparison.csv` with ET-BERT (~50M), YaTC (~30M), FS-Net (~10M), FlowPic (~2M), and TFE-GNN (~5M).
  - [x] **Step 3: Fix Temporal Leakage (Time-Blocked CV)**: Built `src/run_time_blocked_cv.py`; executed 10-block chronological split on ISCX and USTC; verified that Pareto domination holds under strict temporal isolation.
  - [x] **Step 4: Revised Feature Analysis**: Built `src/feature_robustness_experiments.py`; executed TTL perturbation sensitivity (accuracy collapses from 78.7% to 51.8%), dst_port ablation, higher-order IAT moments permutation importance, and feature count diminishing returns curve.
  - [x] **Step 5: Reframe Stability Proofs**: Moved full proofs of Lemma 1 and Lemma 2 to Appendix A; clarified in main text that mathematical swarm stability $\neq$ classifier accuracy.
  - [x] **Step 6: Manuscript Overhaul**: Rewrote title (*"On the Limitations of Multi-Objective Neuro-Evolutionary Traffic Classification in SDWNs: A Negative Result and Lessons Learned"*), abstract, 5-paragraph introduction, and results.
  - [x] **Step 7: Expand Related Work**: Added 15 recent papers (2024–2026) covering adaptive SDN DDoS, concept drift, edge ML, and temporal leakage.
  - [x] **Step 8: Submission Package**: Updated `README.md`, added `Dockerfile`, created Zenodo DOI archiving guide, and verified 13/13 passing automated unit tests.
