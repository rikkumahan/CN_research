# Centralised Memory Store — MOPSO-FFNN-AD Review-2 Project

> [!IMPORTANT]
> **MULTI-AGENT SHARED MEMORY HUB**: This memory system is shared between **Antigravity AI Agent** and **Claude Agent** (and any other developer/agent working in this repository). Always read and update this memory hub before and after making major project changes.

---

## 📌 Quick Navigation

- 🗺️ **[01. Project State & Roadmap](file:///c:/dev/CN_Project/memory/01_PROJECT_STATE_AND_ROADMAP.md)**: Active phase, milestone progress, completed work, and upcoming tasks.
- 📐 **[02. Architecture & Formulas](file:///c:/dev/CN_Project/memory/02_ARCHITECTURE_AND_FORMULAS.md)**: A/B/C framing, FFNN $8 \to 16 \to 8 \to 5$ design, 5-component $F$ equation, Page-Hinkley drift equations, Lemma 1 & 2 stability proofs.
- 📊 **[03. Dataset & Experiment Ledger](file:///c:/dev/CN_Project/memory/03_DATASET_AND_EXPERIMENT_LEDGER.md)**: ISCX VPN/non-VPN (2016) & USTC-TFC (2016) feature schemas, 10-fold CV results, paired t-tests, baseline DL models, ablation, feature importance.
- 🤝 **[04. Agent Handoff Log](file:///c:/dev/CN_Project/memory/04_AGENT_HANDOFF_LOG.md)**: Action history, decision log, handoff checkpoints, and notes for peer agents.

---

## ⚡ Environment & Setup

- **Python Virtual Environment**: `c:\dev\CN_Project\.venv` (Managed via `uv`)
- **Key Installed Packages**: `torch`, `scikit-learn`, `pandas`, `numpy`, `scipy`, `matplotlib`, `pypdf`, `scapy`, `requests`
- **Execution Command**: `uv run python <script_name>.py`

---

## 🎯 Whiteboard Requirements Summary (Review-2)

1. **A**: Base Paper implementation (Pradhan et al. 2022 — single-objective PSO-FFNN).
2. **B**: Senior's Code (Budithi — MOPSO-FFNN-AD on synthetic data).
3. **C**: Upgraded System (Ours — MOPSO-FFNN-AD on real ISCX & USTC datasets + 1D-CNN, LSTM, Transformer baselines + 10-fold CV + ablation + feature importance).
4. **Deliverables**: Code C, Paper text update (`PAPER_SECTION_UPDATES.md`), VTOP PPT slide content (`PRESENTATION_VTOP_SLIDES.md`).

