# AI Agent Handoff Brief: 3-Deck Presentation Generation Guide

> **Recipient Agent**: Claude Agent / PPT Generation Subagent  
> **Authoring Agent**: Antigravity AI Agent  
> **Repository Context**: `c:\dev\CN_Project`  
> **Target Deliverable**: Create 3 clean, professional, presentation-ready slide decks (PowerPoint `.pptx` or structured slide format) covering the entire Review-2 MOPSO-FFNN-AD project.

---

## 🎯 High-Level Mission & Overview

The student is defending their **Capstone / Review-2** project:
**"Multi-Objective Adaptive Traffic Classification in Software-Defined Wireless Networks (MOPSO-FFNN-AD)"**.

To ensure the student is armed for every scenario during faculty questioning, your task is to generate **3 SEPARATE, DEDICATED SLIDE DECKS**:

1. **Deck 1: Main VTOP Review-2 Presentation** (Executive summary of the whole project; 11 slides).
2. **Deck 2: Deep-Dive Results & Viva Defense Deck** (Instruction-by-instruction numerical results, charts, and scripted answers for tricky questions; 10–12 slides).
3. **Deck 3: Technical Code & Architecture Walkthrough Deck** (Step-by-step explanation of *how* the code was implemented, file by file, line by line; 8–10 slides).

---

## 📂 Source Files & Asset Navigation Map

All necessary data, tables, texts, and high-resolution figures have already been generated, verified, and placed in the repository. **Do not fabricate any numbers or invent new metrics.** Everything you need is in these files:

```
c:\dev\CN_Project\
├── docs/
│   ├── PRESENTATION_VTOP_SLIDES.md          <- [Source for Deck 1] 11 clean slides with speaker scripts
│   ├── REVIEW_2_STEP_BY_STEP_RESULTS_GUIDE.md <- [Source for Deck 2] Results, tables, ELI5 & Viva Q&A
│   └── CODE_WALKTHROUGH_HOW_WE_DID_IT.md     <- [Source for Deck 3] Line-by-line code explanation
├── figures/                                  <- [Visual Assets] 300-DPI Publication Figures
│   ├── fig_inst1_dataset_durations.png      <- Inst 1: Flow durations log scale (ISCX & USTC)
│   ├── fig_inst2_dl_params_overhead.png     <- Inst 2: Model parameters log scale (325 vs 18k)
│   ├── fig_inst3_cv_bars_ustc.png           <- Inst 3: 10-fold CV grouped bars for USTC (p=0.0028)
│   ├── fig_inst3_cv_bars_iscx.png           <- Inst 3: 10-fold CV grouped bars for ISCX (p=0.0030)
│   ├── fig_inst4_ablation_policy_bars.png   <- Inst 4: 4-policy Pareto counts & overhead F
│   ├── fig_inst5_feature_importance_comparison.png <- Inst 5: Permutation importance side-by-side
│   ├── fig_inst6_lemma_stability.png        <- Inst 6: Eigenvalues inside unit circle & variance decay
│   ├── fig_inst7_discussion_tradeoffs.png   <- Inst 7: 5-axis radar chart (SDN suitability)
│   └── fig_inst8_system_pipeline.png        <- Inst 8: End-to-end architecture pipeline card
└── results/                                 <- Raw CSV files if you need exact table data
```

---

## 🎨 Slide Design & Formatting Requirements

1. **Clean, Simple Language**:
   - Avoid dense walls of text. Use concise bullet points (maximum 3–4 bullet points per slide).
   - Use plain English words so the student does not stumble during the live presentation.
2. **Professional Color Palette**:
   - **Primary / Headers**: Deep Navy (`#1B365D`)
   - **Accents / Highlights**: Tech Blue (`#2E75B6`), Teal (`#008080`), or Sage Green (`#385723`)
   - **Warning / Alert**: Muted Crimson (`#C00000`)
   - **Card / Background**: Clean White (`#FFFFFF`) or Ultra-Light Gray/Off-White (`#F8F9FA`)
3. **Dedicated Visuals on Every Key Slide**:
   - Embed the exact high-resolution `.png` file specified from `figures/`.
   - Ensure the image has a clear caption and a 1-sentence "Key Takeaway" box below it.
4. **Speaker Notes Included on Every Slide**:
   - Provide a natural, conversational 2–3 sentence "What You Say" script in the slide notes.

---

---

## 📋 Deck 1 Specifications: Main VTOP Review-2 Presentation

**Primary Source**: [`docs/PRESENTATION_VTOP_SLIDES.md`](file:///c:/dev/CN_Project/docs/PRESENTATION_VTOP_SLIDES.md)  
**Target File**: `presentations/Deck1_VTOP_Main_Review2.pptx` (or `.md`)  
**Length**: 11 Slides

### Slide-by-Slide Blueprint:
- **Slide 1: Title Slide**  
  - Title: Multi-Objective Adaptive Traffic Classification in Software-Defined Wireless Networks (MOPSO-FFNN-AD)
  - Subtitle: Review 2: Transition to Real-World Benchmarks, DL Baselines & Statistical Validation
  - Student Details: Budithi Supraja (25MAI0030) | School of Computer Science & Engineering
- **Slide 2: The Three-Tier Comparative Architecture (A vs B vs C)**  
  - Clean comparison table contrasting:
    - Base Paper (A: Pradhan et al. 2022) — Single-objective PSO, accuracy only.
    - Senior's Code (B: Budithi 2024) — Bi-objective MOPSO on synthetic Gaussian data.
    - Upgraded System (C: Ours) — Real PCAPs, DL baselines, 10-fold CV, policy ablation.
- **Slide 3: End-to-End System Pipeline**  
  - Embed: `figures/fig_inst8_system_pipeline.png`
  - 5 core stages: PCAP Ingestion $\to$ 8-Feature Extraction $\to$ Leakage-Free 10-Fold CV $\to$ MOPSO + Drift Detector $\to$ SDWN Controller.
- **Slide 4: Real-World Dataset Benchmarks & Flow Durations**  
  - Embed: `figures/fig_inst1_dataset_durations.png`
  - Key stats: ISCX VPN (3,000 flows, 5 classes) vs USTC-TFC (3,000 flows, 5 classes).
  - Takeaway: Benign traffic finishes in $< 1\text{ ms}$; malware botnets persist for $5\text{ to }9\text{ s}$.
- **Slide 5: Mathematical Rigor & Swarm Stability (Lemmas 1 & 2)**  
  - Embed: `figures/fig_inst6_lemma_stability.png`
  - Lemma 1: Roots lie inside unit circle ($\rho = 0.8543 < 1.0$) $\to$ asymptotic convergence.
  - Lemma 2: Swarm variance decays to zero $\to$ eliminates switch flow-table thrashing.
- **Slide 6: 10-Fold Cross-Validation & Statistical Significance ($p$-values)**  
  - Embed: `figures/fig_inst3_cv_bars_ustc.png` and `figures/fig_inst3_cv_bars_iscx.png`
  - Paired $t$-test against PSO-FFNN: USTC $p = 0.0028 < 0.01$, ISCX $p = 0.0030 < 0.01$.
  - Takeaway: MOPSO's multi-objective trade-off is statistically significant, not random variation.
- **Slide 7: Deep Learning Baseline Comparison (Table 6)**  
  - Embed: `figures/fig_inst2_dl_params_overhead.png`
  - Table: FFNN (325 params) vs 1D-CNN (2,373 params) vs LSTM (13,093 params) vs Transformer (18,437 params).
  - Takeaway: DL models are $7\times\text{ to }56\times$ larger and cannot adapt to concept drift.
- **Slide 8: Policy Weight Ablation (Pareto Analysis)**  
  - Embed: `figures/fig_inst4_ablation_policy_bars.png`
  - 4 scenarios: Default Balanced, Accuracy-Critical, Bandwidth-Constrained, Latency-Sensitive.
  - Takeaway: Latency-sensitive cuts overhead nearly in half ($F \approx 0.36 - 0.42$).
- **Slide 9: Permutation Feature Importance Analysis**  
  - Embed: `figures/fig_inst5_feature_importance_comparison.png`
  - Key findings: `ttl` is #1 for USTC malware; `inter_arrival_time` is #1 for ISCX encrypted traffic; `dst_port` is near-zero because all modern traffic multiplexes over port 443 (HTTPS).
- **Slide 10: Analytical Discussion (Features, Speed, QUIC)**  
  - Embed: `figures/fig_inst7_discussion_tradeoffs.png`
  - 3 pillars: Privacy-preserving statistical features vs raw bytes; offline swarm training vs microsecond inference; resilience to QUIC/TLS 1.3 encryption.
- **Slide 11: Concept Drift Adaptation & Review-2 Conclusion**  
  - Page-Hinkley detector alerts in $< 150\text{ flows}$, triggers warm-restart in $< 2.5\text{ s}$.
  - Verification recap: 13/13 unit tests passed, zero data fabrication, zero data leakage.

---

---

## 📋 Deck 2 Specifications: Results & Viva Defense Guide

**Primary Source**: [`docs/REVIEW_2_STEP_BY_STEP_RESULTS_GUIDE.md`](file:///c:/dev/CN_Project/docs/REVIEW_2_STEP_BY_STEP_RESULTS_GUIDE.md)  
**Target File**: `presentations/Deck2_Results_and_Viva_Defense.pptx` (or `.md`)  
**Length**: 10–12 Slides  
**Core Purpose**: Equip the student to answer tricky faculty questions on specific numbers and charts.

### Key Content Requirements for Deck 2:
1. **Slide Structure for Each Instruction**:
   - Top: High-level metric & visual bar chart.
   - Middle: Exact numerical table (Mean $\pm$ Std, ranges, parameters).
   - Bottom Left: **"Plain English Meaning"** (ELI5 analogy).
   - Bottom Right: **"Professor's Tricky Question & Winning Answer"** box.
2. **Must Cover**:
   - Why 600 flows per class? (Scientific fairness against senior's 3,000 baseline).
   - Why is MOPSO accuracy lower than single-objective PSO? (Multi-objective compromise: trading a small amount of accuracy to prevent switch CPU crashes and TCAM table overflow).
   - Why is `dst_port` useless? (Port 443 HTTPS multiplexing in modern encrypted traffic).
   - What does $p < 0.01$ prove? (Statistically genuine difference, not random lucky splits).
   - Why does Lemma 1 & 2 matter for SDN? (Eliminates flow-table thrashing and southbound message floods).

---

---

## 📋 Deck 3 Specifications: Technical Code Walkthrough

**Primary Source**: [`docs/CODE_WALKTHROUGH_HOW_WE_DID_IT.md`](file:///c:/dev/CN_Project/docs/CODE_WALKTHROUGH_HOW_WE_DID_IT.md)  
**Target File**: `presentations/Deck3_Code_and_Architecture_Walkthrough.pptx` (or `.md`)  
**Length**: 8–10 Slides  
**Core Purpose**: Guide the student during screen sharing if the professor asks: *"Show me your code and where you implemented this."*

### Slide-by-Slide Blueprint:
- **Slide 1: Codebase Architecture & File Structure**  
  - Overview of `src/` modules, `tests/`, `data/`, `results/`, and `figures/`.
- **Slide 2: Data Ingestion & 8-Feature Extraction (`src/dataset_loader.py`)**  
  - Code snippet: 5-tuple flow grouping with Scapy `PcapReader`.
  - Exact formulas for the 8 features: IAT, packet size, protocol, duration, bytes, count, port, TTL.
- **Slide 3: Neural Network Architectures (`src/models.py`)**  
  - Pure NumPy FFNN ($8 \to 16 \to 8 \to 5$): Exact parameter proof $D = 296\text{ weights} + 29\text{ biases} = \mathbf{325}$.
  - PyTorch DL baselines: 1D-CNN (2,373), LSTM (13,093), Transformer (18,437).
- **Slide 4: The 5-Component Composite Fitness $F$ (`src/models.py`)**  
  - Code snippet of `FFNN.composite()`.
  - Explaining $f_1$ (error), $f_2$ (FRUR jitter noise), $f_3$ (CPU load), $f_4$ (setup delay), $f_5$ (bandwidth).
- **Slide 5: Multi-Objective PSO & Pareto Archive (`src/mopso_optimizer.py`)**  
  - What is a particle? (325-dim vector).
  - Code snippet of `dominates()` (Pareto dominance).
  - Crowding distance archive management (capacity: 40) and knee-point selection.
- **Slide 6: Concept Drift Detection (`src/mopso_optimizer.py`)**  
  - Page-Hinkley algorithm: accumulating error rate deviations $U_n - m_n > \lambda=2.0$.
  - Warm-restart MOPSO re-tuning in $< 2.5\text{ seconds}$.
- **Slide 7: 10-Fold CV & Statistical Testing (`src/run_experiments.py`)**  
  - Code snippet: Leakage-free `StandardScaler.fit_transform()` on `X_tr` only.
  - Paired $t$-test implementation via `scipy.stats.ttest_rel()`.
- **Slide 8: Automated Unit Test Suite (`tests/`) & Live Demo Command**  
  - Explaining the 13 automated tests across data pipeline, model parameters, fitness, and optimizer.
  - The live demo command to run: `uv run pytest tests/` ($\to$ 13 passed in 13.40s).

---

---

## 🛠️ Implementation Options for Claude Agent

You can choose either of the following approaches to generate the presentations:

### Option A: Python-PPTX Automated Generation (Recommended for Native `.pptx`)
If generating `.pptx` files directly, you can install `python-pptx` using `uv add python-pptx` and write a Python automation script in `src/generate_pptx_decks.py` that builds the slide decks, formats the typography, sets card backgrounds, embeds the images from `figures/`, and writes speaker notes into each slide's notes slide!

### Option B: Structured Markdown / Marp Slide Decks
If generating presentation markdown files, format them as structured, presentation-ready files in `presentations/Deck1_VTOP_Main_Review2.md`, `presentations/Deck2_Results_and_Viva_Defense.md`, and `presentations/Deck3_Code_and_Architecture_Walkthrough.md` with slide dividers (`---`), clean card blocks, embedded image paths, and clear speaker notes.

---

## 🔒 Non-Negotiable Quality Guardrails
1. **Zero Data Fabrication**: All accuracy numbers, overhead values, and $p$-values must match the CSV files in `results/` and the master guide.
2. **Simple Spoken Language**: Every slide must have conversational speaker notes that empower the student to sound natural and confident.
3. **Visual Embedding**: Link directly to the corresponding figures in `figures/`.

*All the heavy analytical and experimental lifting is done. Build three beautiful, elegant presentations for the student!*

