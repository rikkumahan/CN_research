# Central Memory Index & Guidelines

This repository uses a structured file-based memory system to maintain complete consistency across AI agents (Antigravity and Claude Agent) and human collaborators.

## 📁 Memory Structure

| File | Purpose | Update Frequency |
|---|---|---|
| `MEMORY.md` | Top-level entry point & environment summary | On setup / environment changes |
| `memory/01_PROJECT_STATE_AND_ROADMAP.md` | Execution progress, active task, completed milestones | After every major step / phase |
| `memory/02_ARCHITECTURE_AND_FORMULAS.md` | Models, math equations, loss functions, stability proofs | When changing architecture or math |
| `memory/03_DATASET_AND_EXPERIMENT_LEDGER.md` | Dataset statistics, metrics, CV outputs, t-test tables | When experiment results are generated |
| `memory/04_AGENT_HANDOFF_LOG.md` | Inter-agent activity stream and handoff notes | At the end of every agent turn/session |

## 🛡️ Guidelines for Agents

1. **Read Before Executing**: Before starting any task, read `MEMORY.md` and `memory/01_PROJECT_STATE_AND_ROADMAP.md`.
2. **Never Invent Data**: All metrics in `03_DATASET_AND_EXPERIMENT_LEDGER.md` must be empirically generated and logged from code runs.
3. **Keep Math Exact**: Preserve exact equations from `02_ARCHITECTURE_AND_FORMULAS.md` across paper write-ups and doc updates.
4. **Log Handoffs**: Always log your completed actions in `04_AGENT_HANDOFF_LOG.md` so the next agent (e.g. Claude) can pick up seamlessly.

