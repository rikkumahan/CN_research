# 01. Project State & Roadmap

## Current Status: Phase 1 to Phase 4 Completed & Packaged

### 📌 Milestone Checklist

- [x] **Phase 0 — Setup & Environment**
  - [x] Virtual environment `.venv` created via `uv`
  - [x] Dependencies installed (`torch`, `scikit-learn`, `pandas`, `numpy`, `scipy`, `matplotlib`, `pypdf`, `scapy`, `requests`)
  - [x] Senior PDF (`budithi.pdf`) text extracted (`budithi_extracted.txt`)
  - [x] Centralised memory store created (`MEMORY.md` & `memory/`)
  - [x] Multi-agent instructions created (`AGENTS.md`)

- [x] **Phase 1 — Data Pipeline (`src/dataset_loader.py`)**
  - [x] Ingestion and PCAP streaming flow extraction pipeline built for:
    1. ISCX VPN 2016
    2. USTC-TFC 2016
  - [x] Standard 8-feature schema extractor implemented:
    1. `inter_arrival_time`
    2. `packet_size`
    3. `protocol`
    4. `flow_duration`
    5. `total_bytes`
    6. `packet_count`
    7. `dst_port`
    8. `ttl`
  - [x] Strict leakage prevention: standard scaling fit strictly on training splits.

- [x] **Phase 2 — Core Models & Optimizer (`src/models.py`, `src/mopso_optimizer.py`)**
  - [x] Base Paper PSO-FFNN (A) implemented
  - [x] Senior's MOPSO-FFNN-AD with Page-Hinkley drift detector (B & C) implemented
  - [x] Deep Learning Baselines (C) implemented:
    - 1D-CNN (PyTorch)
    - LSTM (PyTorch)
    - Compact Transformer Encoder (PyTorch)
  - [x] Centralized 5-component fitness calculation $F = \alpha f_1 + \beta \text{FRUR} + \gamma \text{CPU} + \delta \text{FSD} + \epsilon \text{BW}$

- [x] **Phase 3 — Experiments & Statistical Validation (`src/run_experiments.py`)**
  - [x] 10-fold Stratified Cross-Validation runner implemented
  - [x] Statistical paired t-tests (MOPSO-FFNN-AD vs PSO-FFNN) and $p$-value computation
  - [x] 3-policy ablation study ($\alpha=0.8, \epsilon=0.5, \delta=0.5$) implemented
  - [x] Permutation feature importance on all 8 features implemented
  - [x] Publication plotting suite built

- [x] **Phase 4 — Paper & Presentation Assets**
  - [x] Full publication research paper manuscript (`docs/RESEARCH_PAPER_FULL_MANUSCRIPT.md`) with 10 formal sections, proofs, and appendix
  - [x] Publication-grade formatted Word document (`docs/RESEARCH_PAPER_FULL_MANUSCRIPT.docx`, 2.82 MB) with 17 tables and 12 embedded figures
  - [x] Paper updates document (`docs/PAPER_SECTION_UPDATES.md`) with Lemma 1 & 2 proofs, real dataset table, Table 2, Table 6, and 3-point discussion
  - [x] Step-by-Step Results & Plain-English Viva Guide (`docs/REVIEW_2_STEP_BY_STEP_RESULTS_GUIDE.md`)
  - [x] Technical Code Walkthrough Guide (`docs/CODE_WALKTHROUGH_HOW_WE_DID_IT.md`)
  - [x] VTOP PPT presentation slides document (`docs/PRESENTATION_VTOP_SLIDES.md`) comparing A vs B vs C
  - [x] 3 Complete PowerPoint `.pptx` decks generated in `presentations/`
  - [x] 8 High-resolution 300 DPI publication figures in `figures/`
  - [x] GitHub-ready `README.md` and `requirements.txt`


