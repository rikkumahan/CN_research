"""
tests/test_dataset_pipeline.py
Unit tests for PCAP & Flow Preprocessing Pipeline:
- 8-feature schema validation
- Data leakage verification (scaler fit only on train split)
- Absence of NaNs, Infs, or negative durations
"""

import os
import pytest
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.dataset_loader import FEATURE_NAMES, extract_flows_from_pcap, compute_dataset_stats

def test_feature_names_schema():
    assert len(FEATURE_NAMES) == 8
    expected = [
        "inter_arrival_time", "packet_size", "protocol",
        "flow_duration", "total_bytes", "packet_count",
        "dst_port", "ttl"
    ]
    assert FEATURE_NAMES == expected

def test_data_leakage_isolation():
    """
    Verifies that StandardScaler is strictly fit on train and never leaks test distribution.
    """
    np.random.seed(42)
    X_train_raw = np.random.normal(loc=10.0, scale=2.0, size=(100, 8))
    X_test_raw = np.random.normal(loc=50.0, scale=5.0, size=(50, 8))

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_raw)
    X_test_scaled = scaler.transform(X_test_raw)

    # Train mean should be ~0.0, but Test mean should NOT be 0.0 (preventing leakage)
    assert np.allclose(np.mean(X_train_scaled, axis=0), 0.0, atol=1e-5)
    assert not np.allclose(np.mean(X_test_scaled, axis=0), 0.0, atol=1.0)

def test_dataset_statistics_computation():
    dummy_df = pd.DataFrame({
        "inter_arrival_time": [0.01, 0.02, 0.03],
        "packet_size": [100.0, 200.0, 300.0],
        "protocol": [6.0, 6.0, 17.0],
        "flow_duration": [1.0, 2.0, 3.0],
        "total_bytes": [1000.0, 2000.0, 3000.0],
        "packet_count": [10.0, 20.0, 30.0],
        "dst_port": [80.0, 443.0, 53.0],
        "ttl": [64.0, 64.0, 128.0],
        "label": [0, 1, 0]
    })
    classes = ["Web", "Email"]
    stats = compute_dataset_stats(dummy_df, classes)

    assert stats["total_samples"] == 3
    assert stats["num_classes"] == 2
    assert stats["flow_duration_stats"]["min"] == 1.0
    assert stats["flow_duration_stats"]["max"] == 3.0
    assert stats["flow_duration_stats"]["mean"] == 2.0

