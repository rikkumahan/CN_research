# AGENTS.md — Multi-Agent Operating Instructions & Repository Rules

> [!IMPORTANT]
> **MANDATORY FOR ALL AI AGENTS**: Any AI agent (Antigravity Agent, Claude Agent, Cursor Agent, etc.) operating in this repository MUST read this file and `MEMORY.md` before executing any commands or modifying code.

---

## 1. Project Overview & Objective

This repository contains the **MOPSO-FFNN-AD** Software-Defined Wireless Network (SDWN) traffic classification research project. The goal for Review 2 is to strengthen the paper (`budithi.pdf`) and code (`MOPSO_FFNN_AD_FINAL - Budithi Supraja 25MAI0030.py`) by transitioning from synthetic data to real traffic benchmarks (ISCX VPN 2016 & USTC-TFC 2016), adding deep learning baselines (1D-CNN, LSTM, Transformer), conducting 10-fold stratified cross-validation with statistical significance tests ($p$-values), performing policy weight ablation, and generating publication assets.

---

## 2. System Architecture Framing (Whiteboard A / B / C)

All agents must adhere to the three-tier experimental comparison framework:

- **A (Base Paper)**: Pradhan et al. (IET 2022) — Single-objective PSO-FFNN optimizing accuracy.
- **B (Senior's Code)**: Budithi Supraja (2024/2025) — MOPSO-FFNN-AD on synthetic dataset (3,000 samples).
- **C (Upgraded System - Ours)**: MOPSO-FFNN-AD on real ISCX & USTC datasets + 1D-CNN, LSTM, and Transformer baselines + 10-fold CV + 3-policy ablation + feature importance.

---

## 3. Environment & Execution Protocol

- **Virtual Environment**: `.venv` at project root.
- **Package Manager**: Always use `uv` for running scripts and installing packages:
  ```bash
  uv run python <script_name>.py
  ```
- **Key Installed Packages**: `torch`, `scikit-learn`, `pandas`, `numpy`, `scipy`, `matplotlib`, `pypdf`, `scapy`, `requests`.

---

## 4. Centralised Memory Protocol

Before starting work:
1. Read `MEMORY.md` at project root.
2. Read `memory/01_PROJECT_STATE_AND_ROADMAP.md` to identify current phase and open tasks.
3. Read `memory/04_AGENT_HANDOFF_LOG.md` to see previous agent actions.

After completing work:
1. Record all generated metrics/figures in `memory/03_DATASET_AND_EXPERIMENT_LEDGER.md`.
2. Update task completion status in `memory/01_PROJECT_STATE_AND_ROADMAP.md`.
3. Append a brief summary of your work and next steps in `memory/04_AGENT_HANDOFF_LOG.md`.

---

## 5. Non-Negotiable Rules for Agents

1. **Zero Data Fabrication**: Never invent accuracy numbers, $F$-fitness values, or $p$-values. All numbers in tables must come directly from execution logs.
2. **Strict Leakage Prevention**: Normalization (`StandardScaler`) must be fit ONLY on the training fold within each cross-validation split.
3. **Preserve Mathematical Rigor**: Keep exact equation representations for $F$-fitness, Page-Hinkley drift, Lemma 1 (first-order convergence), and Lemma 2 (variance convergence).
4. **Reproducibility**: Save random seed (`seed=42`), config parameters, raw fold outputs, and clean logs for every experiment run.

