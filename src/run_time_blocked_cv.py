"""
src/run_time_blocked_cv.py
Temporal Leakage-Free Evaluation via Time-Based Blocking Cross-Validation:
- Replaces random stratified K-Fold with 10 contiguous chronological time blocks
- Prevents session/burst temporal autocorrelation leakage
- Fits StandardScaler strictly on training folds
- Evaluates PSO-FFNN, MOPSO-FFNN-AD, 1D-CNN, LSTM, and Transformer
- Computes paired two-tailed t-tests (vs PSO-FFNN) and saves publication results
"""

import os
import sys
import time
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.models import (
    FFNN, PyTorchCNN1D, PyTorchLSTM, PyTorchTransformer,
    DeepLearningWrapper, DEFAULT_WEIGHTS
)
from src.mopso_optimizer import pso_run, mopso_run, deploy_knee
from src.dataset_loader import load_processed_data

RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
FIGURES_DIR = os.path.join(PROJECT_ROOT, "figures")
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

SEED = 42
np.random.seed(SEED)


def generate_time_blocked_splits(y, n_blocks=10):
    """
    Partitions sequentially ordered dataset into n_blocks contiguous time blocks per class.
    Yields (train_indices, test_indices) for each block.
    """
    classes = np.unique(y)
    class_indices = {c: np.where(y == c)[0] for c in classes}
    
    splits = []
    for b in range(n_blocks):
        test_idx = []
        train_idx = []
        for c in classes:
            c_idx = class_indices[c]
            block_sz = len(c_idx) // n_blocks
            b_start = b * block_sz
            b_end = (b + 1) * block_sz if b < n_blocks - 1 else len(c_idx)
            
            test_c = c_idx[b_start:b_end]
            train_c = np.concatenate([c_idx[:b_start], c_idx[b_end:]])
            
            test_idx.extend(test_c)
            train_idx.extend(train_c)
            
        splits.append((np.array(train_idx), np.array(test_idx)))
    return splits


def run_time_blocked_cv(dataset_name="iscx", n_blocks=10):
    print("\n" + "=" * 75, flush=True)
    print(f" [RUNNING TIME-BASED BLOCKING CV (LEAK-FREE)] ON {dataset_name.upper()}", flush=True)
    print("=" * 75, flush=True)

    X_raw, y, class_names = load_processed_data(dataset_name)
    num_classes = len(class_names)
    splits = generate_time_blocked_splits(y, n_blocks=n_blocks)

    fold_records = []
    ffnn = FFNN(ni=8, h1=16, h2=8, no=num_classes)

    for block_idx, (train_idx, test_idx) in enumerate(splits):
        print(f"\n>>> Time Block {block_idx + 1}/{n_blocks} (Train: {len(train_idx)}, Test: {len(test_idx)}) <<<", flush=True)
        X_tr_raw, y_tr = X_raw[train_idx], y[train_idx]
        X_te_raw, y_te = X_raw[test_idx], y[test_idx]

        # Log-transform continuous features, then fit scaler strictly on train split
        X_tr_log = np.log1p(np.maximum(X_tr_raw, 0.0))
        X_te_log = np.log1p(np.maximum(X_te_raw, 0.0))

        scaler = StandardScaler()
        X_tr = scaler.fit_transform(X_tr_log)
        X_te = scaler.transform(X_te_log)

        n_val = max(int(len(X_tr) * 0.12), 30)
        X_val, y_val = X_tr[:n_val], y_tr[:n_val]
        X_fit, y_fit = X_tr[n_val:], y_tr[n_val:]

        # 1. PSO-FFNN (Base Paper A)
        t0 = time.time()
        pso_w, _ = pso_run(ffnn, X_fit, y_fit, n_p=35, T=180, verbose=False)
        pso_time = time.time() - t0
        pso_acc = ffnn.acc(X_te, y_te, pso_w)
        pso_F, *_ = ffnn.composite(X_te, y_te, pso_w)

        fold_records.append({
            "block": block_idx + 1, "model": "PSO-FFNN (A)",
            "accuracy": pso_acc, "F": pso_F, "train_time": pso_time,
            "params": ffnn.D
        })

        # 2. MOPSO-FFNN-AD (Proposed C)
        t0 = time.time()
        arc, _, _ = mopso_run(ffnn, X_fit, y_fit, X_val, pso_w, n_p=40, T=150, amax=35, verbose=False)
        mopso_time = time.time() - t0 + pso_time
        knee = deploy_knee(arc, ffnn, X_fit, y_fit)
        mopso_w = knee[0]
        mopso_acc = ffnn.acc(X_te, y_te, mopso_w)
        mopso_F, *_ = ffnn.composite(X_te, y_te, mopso_w)

        fold_records.append({
            "block": block_idx + 1, "model": "MOPSO-FFNN-AD (C)",
            "accuracy": mopso_acc, "F": mopso_F, "train_time": mopso_time,
            "params": ffnn.D
        })

        # 3. 1D-CNN Baseline
        cnn = DeepLearningWrapper(PyTorchCNN1D, name="CNN-1D", epochs=25, num_classes=num_classes)
        cnn.fit(X_fit, y_fit)
        cnn_metrics = cnn.evaluate(X_te, y_te)
        cnn_F, *_ = cnn.compute_composite_overhead(X_te, y_te)

        fold_records.append({
            "block": block_idx + 1, "model": "CNN-1D",
            "accuracy": cnn_metrics["accuracy"], "F": cnn_F,
            "train_time": cnn.train_time, "params": cnn.count_parameters()
        })

        # 4. LSTM Baseline
        lstm = DeepLearningWrapper(PyTorchLSTM, name="LSTM", epochs=25, num_classes=num_classes)
        lstm.fit(X_fit, y_fit)
        lstm_metrics = lstm.evaluate(X_te, y_te)
        lstm_F, *_ = lstm.compute_composite_overhead(X_te, y_te)

        fold_records.append({
            "block": block_idx + 1, "model": "LSTM",
            "accuracy": lstm_metrics["accuracy"], "F": lstm_F,
            "train_time": lstm.train_time, "params": lstm.count_parameters()
        })

        # 5. Transformer Baseline
        trf = DeepLearningWrapper(PyTorchTransformer, name="Transformer", epochs=25, num_classes=num_classes)
        trf.fit(X_fit, y_fit)
        trf_metrics = trf.evaluate(X_te, y_te)
        trf_F, *_ = trf.compute_composite_overhead(X_te, y_te)

        fold_records.append({
            "block": block_idx + 1, "model": "Transformer",
            "accuracy": trf_metrics["accuracy"], "F": trf_F,
            "train_time": trf.train_time, "params": trf.count_parameters()
        })

        print(f"  PSO-FFNN:   Acc={pso_acc:.4f}  F={pso_F:.4f}")
        print(f"  MOPSO-FFNN: Acc={mopso_acc:.4f}  F={mopso_F:.4f}")
        print(f"  CNN-1D:     Acc={cnn_metrics['accuracy']:.4f}  F={cnn_F:.4f}")
        print(f"  LSTM:       Acc={lstm_metrics['accuracy']:.4f}  F={lstm_F:.4f}")
        print(f"  Transformer:Acc={trf_metrics['accuracy']:.4f}  F={trf_F:.4f}")

    df_blocks = pd.DataFrame(fold_records)
    raw_csv = os.path.join(RESULTS_DIR, f"time_blocked_cv_raw_{dataset_name}.csv")
    df_blocks.to_csv(raw_csv, index=False)

    # Statistical Aggregation
    pso_accs = df_blocks[df_blocks["model"] == "PSO-FFNN (A)"]["accuracy"].values
    pso_Fs = df_blocks[df_blocks["model"] == "PSO-FFNN (A)"]["F"].values

    summary_rows = []
    models = ["PSO-FFNN (A)", "MOPSO-FFNN-AD (C)", "CNN-1D", "LSTM", "Transformer"]

    for m in models:
        m_df = df_blocks[df_blocks["model"] == m]
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
    table_file = os.path.join(RESULTS_DIR, f"table2_time_blocked_cv_{dataset_name}.csv")
    df_summary.to_csv(table_file, index=False)

    print("\n" + "=" * 75)
    print(f" TIME-BLOCKED CV SUMMARY FOR {dataset_name.upper()} (DELIVERABLE STEP 3)")
    print("=" * 75)
    print(df_summary.to_string(index=False))

    # Publication boxplot
    plt.figure(figsize=(10, 5))
    acc_data = [df_blocks[df_blocks["model"] == m]["accuracy"].values for m in models]
    plt.boxplot(acc_data, tick_labels=models, patch_artist=True,
                boxprops=dict(facecolor='#4C72B0', alpha=0.7),
                medianprops=dict(color='red', lw=2))
    plt.ylabel("Time-Blocked Test Accuracy", fontsize=11)
    plt.title(f"Time-Blocked Cross-Validation Accuracy ({dataset_name.upper()})", fontsize=12)
    plt.grid(True, ls='--', alpha=0.3)
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, f"fig_time_blocked_cv_accuracy_{dataset_name}.png")
    plt.savefig(fig_path, dpi=150)
    plt.close()
    print(f"[OK] Figure saved -> {fig_path}")

    return df_summary, df_blocks


if __name__ == "__main__":
    df_iscx, _ = run_time_blocked_cv("iscx", n_blocks=10)
    df_ustc, _ = run_time_blocked_cv("ustc", n_blocks=10)
    print("\n[STEP 3 TIME-BLOCKED CROSS-VALIDATION FINISHED SUCCESSFULLY!]")
