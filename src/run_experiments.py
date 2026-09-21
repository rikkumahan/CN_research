"""
src/run_experiments.py
Master Experimental Suite for Review-2:
1. 10-Fold Stratified Cross-Validation (Leakage-free standard scaling)
2. Paired t-tests (MOPSO-FFNN-AD vs PSO-FFNN) with exact p-values
3. SOTA Baseline Comparison (FFNN, 1D-CNN, LSTM, Transformer)
4. 3-Policy Fitness Weight Ablation (Accuracy-Critical, Bandwidth-Constrained, Latency-Sensitive)
5. Permutation Feature Importance Analysis
6. Publication-ready figure generation
"""

import os
import sys
import json
import time

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from src.models import (
    FFNN, PyTorchCNN1D, PyTorchLSTM, PyTorchTransformer,
    DeepLearningWrapper, DEFAULT_WEIGHTS
)
from src.mopso_optimizer import pso_run, mopso_run, deploy_knee, PageHinkley
from src.dataset_loader import load_processed_data, FEATURE_NAMES

BASE_DIR = PROJECT_ROOT
RESULTS_DIR = os.path.join(BASE_DIR, "results")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

SEED = 42
np.random.seed(SEED)

# ----------------------------------------------------------------------
# 1. 10-Fold Stratified Cross-Validation & Statistical Testing
# ----------------------------------------------------------------------
def run_10fold_cross_validation(dataset_name="iscx", n_splits=10):
    print("\n" + "=" * 70, flush=True)
    print(f" [1] RUNNING 10-FOLD STRATIFIED CROSS-VALIDATION ON {dataset_name.upper()}", flush=True)
    print("=" * 70, flush=True)

    X_raw, y, class_names = load_processed_data(dataset_name)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    num_classes = len(class_names)

    fold_records = []
    ffnn = FFNN(ni=8, h1=16, h2=8, no=num_classes)

    for fold, (train_idx, test_idx) in enumerate(skf.split(X_raw, y)):
        print(f"\n--- Fold {fold + 1}/{n_splits} ---", flush=True)
        X_tr_raw, y_tr = X_raw[train_idx], y[train_idx]
        X_te_raw, y_te = X_raw[test_idx], y[test_idx]

        # Apply log1p transform to skewed network continuous features then standard scale
        X_tr_log = np.log1p(np.maximum(X_tr_raw, 0.0))
        X_te_log = np.log1p(np.maximum(X_te_raw, 0.0))

        # Strict leakage prevention: fit scaler ONLY on train fold
        scaler = StandardScaler()
        X_tr = scaler.fit_transform(X_tr_log)
        X_te = scaler.transform(X_te_log)

        # Validation split from train for FRUR
        n_val = max(int(len(X_tr) * 0.12), 30)
        X_val, y_val = X_tr[:n_val], y_tr[:n_val]
        X_fit, y_fit = X_tr[n_val:], y_tr[n_val:]

        # A: PSO-FFNN (Base Paper)
        t0 = time.time()
        pso_w, _ = pso_run(ffnn, X_fit, y_fit, n_p=40, T=250, verbose=False)
        pso_time = time.time() - t0
        pso_acc = ffnn.acc(X_te, y_te, pso_w)
        pso_F, *_ = ffnn.composite(X_te, y_te, pso_w)

        fold_records.append({
            "fold": fold + 1, "model": "PSO-FFNN (A)",
            "accuracy": pso_acc, "F": pso_F, "train_time": pso_time,
            "params": ffnn.D
        })

        # C: MOPSO-FFNN-AD (Proposed Upgraded)
        t0 = time.time()
        arc, _, _ = mopso_run(ffnn, X_fit, y_fit, X_val, pso_w, n_p=45, T=200, amax=40, verbose=False)
        mopso_time = time.time() - t0 + pso_time
        knee = deploy_knee(arc, ffnn, X_fit, y_fit)
        mopso_w = knee[0]
        mopso_acc = ffnn.acc(X_te, y_te, mopso_w)
        mopso_F, *_ = ffnn.composite(X_te, y_te, mopso_w)

        fold_records.append({
            "fold": fold + 1, "model": "MOPSO-FFNN-AD (C)",
            "accuracy": mopso_acc, "F": mopso_F, "train_time": mopso_time,
            "params": ffnn.D
        })

        # C-Baselines: 1D-CNN
        cnn = DeepLearningWrapper(PyTorchCNN1D, name="CNN-1D", epochs=30, num_classes=num_classes)
        cnn.fit(X_fit, y_fit)
        cnn_metrics = cnn.evaluate(X_te, y_te)
        cnn_F, *_ = cnn.compute_composite_overhead(X_te, y_te)

        fold_records.append({
            "fold": fold + 1, "model": "CNN-1D",
            "accuracy": cnn_metrics["accuracy"], "F": cnn_F,
            "train_time": cnn.train_time, "params": cnn.count_parameters()
        })

        # C-Baselines: LSTM
        lstm = DeepLearningWrapper(PyTorchLSTM, name="LSTM", epochs=30, num_classes=num_classes)
        lstm.fit(X_fit, y_fit)
        lstm_metrics = lstm.evaluate(X_te, y_te)
        lstm_F, *_ = lstm.compute_composite_overhead(X_te, y_te)

        fold_records.append({
            "fold": fold + 1, "model": "LSTM",
            "accuracy": lstm_metrics["accuracy"], "F": lstm_F,
            "train_time": lstm.train_time, "params": lstm.count_parameters()
        })

        # C-Baselines: Transformer
        trf = DeepLearningWrapper(PyTorchTransformer, name="Transformer", epochs=30, num_classes=num_classes)
        trf.fit(X_fit, y_fit)
        trf_metrics = trf.evaluate(X_te, y_te)
        trf_F, *_ = trf.compute_composite_overhead(X_te, y_te)

        fold_records.append({
            "fold": fold + 1, "model": "Transformer",
            "accuracy": trf_metrics["accuracy"], "F": trf_F,
            "train_time": trf.train_time, "params": trf.count_parameters()
        })

        print(f"  PSO-FFNN:   Acc={pso_acc:.4f}  F={pso_F:.4f}", flush=True)
        print(f"  MOPSO-FFNN: Acc={mopso_acc:.4f}  F={mopso_F:.4f}", flush=True)
        print(f"  CNN-1D:     Acc={cnn_metrics['accuracy']:.4f}  F={cnn_F:.4f}", flush=True)
        print(f"  LSTM:       Acc={lstm_metrics['accuracy']:.4f}  F={lstm_F:.4f}", flush=True)
        print(f"  Transformer:Acc={trf_metrics['accuracy']:.4f}  F={trf_F:.4f}", flush=True)

    df_folds = pd.DataFrame(fold_records)
    df_folds.to_csv(os.path.join(RESULTS_DIR, f"cv_10fold_raw_{dataset_name}.csv"), index=False)

    # Statistical Aggregation & Paired t-tests vs PSO-FFNN
    pso_accs = df_folds[df_folds["model"] == "PSO-FFNN (A)"]["accuracy"].values
    pso_Fs = df_folds[df_folds["model"] == "PSO-FFNN (A)"]["F"].values

    summary_rows = []
    models = ["PSO-FFNN (A)", "MOPSO-FFNN-AD (C)", "CNN-1D", "LSTM", "Transformer"]

    for m in models:
        m_df = df_folds[df_folds["model"] == m]
        acc_vals = m_df["accuracy"].values
        F_vals = m_df["F"].values
        params = m_df["params"].iloc[0]

        if m == "PSO-FFNN (A)":
            t_acc, p_acc = np.nan, np.nan
            t_F, p_F = np.nan, np.nan
        else:
            t_acc, p_acc = stats.ttest_rel(acc_vals, pso_accs)
            t_F, p_F = stats.ttest_rel(F_vals, pso_Fs)

        summary_rows.append({
            "Method": m,
            "Accuracy (mean ± std)": f"{np.mean(acc_vals):.4f} ± {np.std(acc_vals):.4f}",
            "Overhead F (mean ± std)": f"{np.mean(F_vals):.4f} ± {np.std(F_vals):.4f}",
            "t-stat (Acc vs PSO)": f"{t_acc:.3f}" if not np.isnan(t_acc) else "-",
            "p-val (Acc)": f"{p_acc:.4e}" if not np.isnan(p_acc) else "-",
            "t-stat (F vs PSO)": f"{t_F:.3f}" if not np.isnan(t_F) else "-",
            "p-val (F)": f"{p_F:.4e}" if not np.isnan(p_F) else "-",
            "Params": params
        })

    df_summary = pd.DataFrame(summary_rows)
    table2_file = os.path.join(RESULTS_DIR, f"table2_10fold_cv_{dataset_name}.csv")
    df_summary.to_csv(table2_file, index=False)

    print("\n" + "=" * 70)
    print(" UPDATED TABLE 2 — 10-FOLD CV METRICS & STATISTICAL SIGNIFICANCE")
    print("=" * 70)
    print(df_summary.to_string(index=False))

    # Boxplot figure
    plt.figure(figsize=(10, 5))
    acc_data = [df_folds[df_folds["model"] == m]["accuracy"].values for m in models]
    try:
        plt.boxplot(acc_data, tick_labels=models, patch_artist=True,
                    boxprops=dict(facecolor='#4C72B0', alpha=0.7),
                    medianprops=dict(color='red', lw=2))
    except TypeError:
        plt.boxplot(acc_data, labels=models, patch_artist=True,
                    boxprops=dict(facecolor='#4C72B0', alpha=0.7),
                    medianprops=dict(color='red', lw=2))
    plt.ylabel("10-Fold Test Accuracy", fontsize=11)
    plt.title(f"10-Fold Stratified Cross-Validation Accuracy Distribution ({dataset_name.upper()})", fontsize=12)
    plt.grid(True, ls='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, f"fig_cv_accuracy_boxplots_{dataset_name}.png"), dpi=150)
    plt.close()

    return df_summary, df_folds


# ----------------------------------------------------------------------
# 2. 3-Policy Fitness Weight Ablation Study
# ----------------------------------------------------------------------
def run_ablation_study(dataset_name="iscx"):
    print("\n" + "=" * 70)
    print(f" [2] RUNNING FITNESS-WEIGHT ABLATION STUDY (3 POLICIES) ON {dataset_name.upper()}")
    print("=" * 70)

    X_raw, y, class_names = load_processed_data(dataset_name)
    scaler = StandardScaler()
    X = scaler.fit_transform(np.log1p(np.maximum(X_raw, 0.0)))

    n_split = int(len(X) * 0.8)
    X_fit, y_fit = X[:n_split], y[:n_split]
    X_te, y_te = X[n_split:], y[n_split:]
    X_val = X_fit[:int(len(X_fit) * 0.15)]

    ffnn = FFNN(ni=8, h1=16, h2=8, no=len(class_names))
    pso_w, _ = pso_run(ffnn, X_fit, y_fit, n_p=40, T=200, verbose=False)

    policies = {
        "Default (Balanced)": {
            'weights': {'alpha': 0.45, 'beta': 0.20, 'gamma': 0.15, 'delta': 0.10, 'epsilon': 0.10},
            'color': '#2E75B6', 'marker': 'o'
        },
        "Accuracy-Critical": {
            'weights': {'alpha': 0.80, 'beta': 0.08, 'gamma': 0.06, 'delta': 0.03, 'epsilon': 0.03},
            'color': '#C44E52', 'marker': 's'
        },
        "Bandwidth-Constrained": {
            'weights': {'alpha': 0.25, 'beta': 0.10, 'gamma': 0.10, 'delta': 0.05, 'epsilon': 0.50},
            'color': '#55A868', 'marker': '^'
        },
        "Latency-Sensitive": {
            'weights': {'alpha': 0.25, 'beta': 0.10, 'gamma': 0.10, 'delta': 0.50, 'epsilon': 0.05},
            'color': '#8172B2', 'marker': 'D'
        }
    }

    plt.figure(figsize=(10, 6))
    ablation_records = []

    for pname, pinfo in policies.items():
        w = pinfo['weights']
        arc, _, _ = mopso_run(ffnn, X_fit, y_fit, X_val, pso_w, weights=w, n_p=45, T=200, amax=40, verbose=False)
        knee = deploy_knee(arc, ffnn, X_fit, y_fit)

        accs = np.array([ffnn.acc(X_te, y_te, s[0]) for s in arc])
        Fs = np.array([ffnn.composite(X_te, y_te, s[0], weights=w)[0] for s in arc])
        o = np.argsort(Fs)

        plt.plot(Fs[o], accs[o], ls='--', color=pinfo['color'], alpha=0.5)
        plt.scatter(Fs, accs, label=f"{pname} (Archive: {len(arc)})",
                    color=pinfo['color'], marker=pinfo['marker'], s=80, alpha=0.85)

        # Plot deployed knee
        knee_acc = ffnn.acc(X_te, y_te, knee[0])
        knee_F = ffnn.composite(X_te, y_te, knee[0], weights=w)[0]
        plt.scatter(knee_F, knee_acc, color=pinfo['color'], edgecolors='black',
                    s=220, marker='*', zorder=10)

        ablation_records.append({
            "Policy": pname,
            "Weights (alpha, beta, gamma, delta, epsilon)": f"{w['alpha']}/{w['beta']}/{w['gamma']}/{w['delta']}/{w['epsilon']}",
            "Deployed_Acc": round(knee_acc, 4),
            "Deployed_F": round(knee_F, 4),
            "Pareto_Solutions": len(arc),
            "Acc_Range": f"[{accs.min():.4f}, {accs.max():.4f}]",
            "F_Range": f"[{Fs.min():.4f}, {Fs.max():.4f}]"
        })

    plt.xlabel("Composite Overhead F ↓", fontsize=11)
    plt.ylabel("Test Accuracy ↑", fontsize=11)
    plt.title(f"Pareto Front Shift Under 3 Deployment Policies vs Default ({dataset_name.upper()})", fontsize=12)
    plt.legend(fontsize=9, loc="lower right")
    plt.grid(True, ls='--', alpha=0.3)
    plt.tight_layout()

    fig_file = os.path.join(FIGURES_DIR, f"fig_pareto_ablation_{dataset_name}.png")
    plt.savefig(fig_file, dpi=150)
    plt.close()

    df_ablation = pd.DataFrame(ablation_records)
    df_ablation.to_csv(os.path.join(RESULTS_DIR, f"ablation_policies_{dataset_name}.csv"), index=False)
    print(df_ablation.to_string(index=False))
    print(f" Saved Pareto Ablation figure -> {fig_file}")


# ----------------------------------------------------------------------
# 3. Permutation Feature Importance Analysis
# ----------------------------------------------------------------------
def run_feature_importance(dataset_name="iscx", n_repeats=10):
    print("\n" + "=" * 70)
    print(f" [3] RUNNING PERMUTATION FEATURE IMPORTANCE ANALYSIS ON {dataset_name.upper()}")
    print("=" * 70)

    X_raw, y, class_names = load_processed_data(dataset_name)
    scaler = StandardScaler()
    X = scaler.fit_transform(np.log1p(np.maximum(X_raw, 0.0)))

    n_split = int(len(X) * 0.8)
    X_fit, y_fit = X[:n_split], y[:n_split]
    X_te, y_te = X[n_split:], y[n_split:]
    X_val = X_fit[:int(len(X_fit) * 0.15)]

    ffnn = FFNN(ni=8, h1=16, h2=8, no=len(class_names))
    pso_w, _ = pso_run(ffnn, X_fit, y_fit, n_p=40, T=200, verbose=False)
    arc, _, _ = mopso_run(ffnn, X_fit, y_fit, X_val, pso_w, n_p=45, T=200, amax=40, verbose=False)
    knee = deploy_knee(arc, ffnn, X_fit, y_fit)
    best_w = knee[0]

    baseline_acc = ffnn.acc(X_te, y_te, best_w)
    baseline_F = ffnn.composite(X_te, y_te, best_w)[0]

    importance_records = []
    for f_idx, fname in enumerate(FEATURE_NAMES):
        acc_drops = []
        F_deltas = []
        for _ in range(n_repeats):
            X_perm = X_te.copy()
            X_perm[:, f_idx] = np.random.permutation(X_perm[:, f_idx])
            perm_acc = ffnn.acc(X_perm, y_te, best_w)
            perm_F = ffnn.composite(X_perm, y_te, best_w)[0]

            acc_drops.append(max(0.0, baseline_acc - perm_acc))
            F_deltas.append(perm_F - baseline_F)

        importance_records.append({
            "Feature": fname,
            "Accuracy_Drop_Mean": float(np.mean(acc_drops)),
            "Accuracy_Drop_Std": float(np.std(acc_drops)),
            "F_Delta_Mean": float(np.mean(F_deltas)),
            "F_Delta_Std": float(np.std(F_deltas))
        })

    df_imp = pd.DataFrame(importance_records).sort_values(by="Accuracy_Drop_Mean", ascending=False)
    df_imp.to_csv(os.path.join(RESULTS_DIR, f"feature_importance_{dataset_name}.csv"), index=False)

    print("\n--- FEATURE IMPORTANCE TABLE ---")
    print(df_imp.to_string(index=False))

    # Bar chart
    plt.figure(figsize=(9, 5))
    y_pos = np.arange(len(df_imp))
    plt.barh(y_pos, df_imp["Accuracy_Drop_Mean"], xerr=df_imp["Accuracy_Drop_Std"],
             color='#2E75B6', edgecolor='navy', alpha=0.85, capsize=4)
    plt.yticks(y_pos, df_imp["Feature"], fontsize=10)
    plt.gca().invert_yaxis()
    plt.xlabel("Permutation Importance (Accuracy Degradation)", fontsize=11)
    plt.title(f"Feature Importance via Permutation Analysis ({dataset_name.upper()})", fontsize=12)
    plt.grid(True, ls='--', alpha=0.3)
    plt.tight_layout()

    fig_file = os.path.join(FIGURES_DIR, f"fig_feature_importance_{dataset_name}.png")
    plt.savefig(fig_file, dpi=150)
    plt.close()
    print(f" Saved Feature Importance figure -> {fig_file}")


# ----------------------------------------------------------------------
# 4. Generate Complete Updated SOTA Table 6
# ----------------------------------------------------------------------
def generate_table6_sota(cv_summary_df):
    print("\n" + "=" * 70)
    print(" [4] GENERATING UPDATED SOTA COMPARISON (TABLE 6)")
    print("=" * 70)

    sota_rows = [
        {"Method": "DBN (Shao et al. [7])", "Accuracy": "96.00% (lit)", "Overhead F": "N/A", "Params": "N/A", "Concept Drift": "No", "Multi-Objective": "No"},
        {"Method": "RNN (Wang et al. [12])", "Accuracy": "94.00% (lit)", "Overhead F": "N/A", "Params": "N/A", "Concept Drift": "No", "Multi-Objective": "No"},
        {"Method": "1D-CNN (Ours Baseline)", "Accuracy": cv_summary_df[cv_summary_df["Method"] == "CNN-1D"]["Accuracy (mean ± std)"].iloc[0], "Overhead F": cv_summary_df[cv_summary_df["Method"] == "CNN-1D"]["Overhead F (mean ± std)"].iloc[0], "Params": "2,373", "Concept Drift": "No", "Multi-Objective": "No"},
        {"Method": "LSTM (Ours Baseline)", "Accuracy": cv_summary_df[cv_summary_df["Method"] == "LSTM"]["Accuracy (mean ± std)"].iloc[0], "Overhead F": cv_summary_df[cv_summary_df["Method"] == "LSTM"]["Overhead F (mean ± std)"].iloc[0], "Params": "13,093", "Concept Drift": "No", "Multi-Objective": "No"},
        {"Method": "Transformer (Ours Baseline)", "Accuracy": cv_summary_df[cv_summary_df["Method"] == "Transformer"]["Accuracy (mean ± std)"].iloc[0], "Overhead F": cv_summary_df[cv_summary_df["Method"] == "Transformer"]["Overhead F (mean ± std)"].iloc[0], "Params": "18,437", "Concept Drift": "No", "Multi-Objective": "No"},
        {"Method": "PSO-FFNN (Base Paper [2])", "Accuracy": cv_summary_df[cv_summary_df["Method"] == "PSO-FFNN (A)"]["Accuracy (mean ± std)"].iloc[0], "Overhead F": cv_summary_df[cv_summary_df["Method"] == "PSO-FFNN (A)"]["Overhead F (mean ± std)"].iloc[0], "Params": "325", "Concept Drift": "No", "Multi-Objective": "No"},
        {"Method": "MOPSO-FFNN-AD (Senior [B-Synth])", "Accuracy": "94.33%", "Overhead F": "0.2697", "Params": "325", "Concept Drift": "Yes (PH)", "Multi-Objective": "Yes (6 Sols)"},
        {"Method": "MOPSO-FFNN-AD (Ours [C-Real])", "Accuracy": cv_summary_df[cv_summary_df["Method"] == "MOPSO-FFNN-AD (C)"]["Accuracy (mean ± std)"].iloc[0], "Overhead F": cv_summary_df[cv_summary_df["Method"] == "MOPSO-FFNN-AD (C)"]["Overhead F (mean ± std)"].iloc[0], "Params": "325", "Concept Drift": "Yes (PH)", "Multi-Objective": "Yes (Pareto)"},
    ]

    df_sota = pd.DataFrame(sota_rows)
    table6_path = os.path.join(RESULTS_DIR, "table6_sota_comparison.csv")
    df_sota.to_csv(table6_path, index=False)
    print(df_sota.to_string(index=False))
    print(f"\n Deliverable Ready: Saved {table6_path}")


if __name__ == "__main__":
    # Run 10-fold CV on ISCX VPN 2016
    df_cv_iscx, _ = run_10fold_cross_validation(dataset_name="iscx", n_splits=10)
    run_ablation_study(dataset_name="iscx")
    run_feature_importance(dataset_name="iscx")
    generate_table6_sota(df_cv_iscx)

    # Run 10-fold CV on USTC-TFC 2016
    df_cv_ustc, _ = run_10fold_cross_validation(dataset_name="ustc", n_splits=10)
    run_ablation_study(dataset_name="ustc")
    run_feature_importance(dataset_name="ustc")
    print("\n[ALL EXPERIMENTS COMPLETED SUCCESSFULLY!]")
