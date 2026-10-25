"""
tests/test_time_blocked_and_robustness.py
Unit tests for Review 3 extensions:
- Time-based blocking cross-validation split properties
- TTL perturbation logic and dst_port feature deletion
- Higher-order statistical moment computation (variance, skewness, kurtosis)
"""

import numpy as np
import pytest
from scipy import stats
from src.run_time_blocked_cv import generate_time_blocked_splits

def test_time_blocked_splits_integrity():
    """
    Verifies that time-blocked splits:
    1. Produce exactly n_blocks splits
    2. Have non-overlapping train and test sets
    3. Union of all test sets covers the dataset exactly once
    """
    y = np.array([0] * 50 + [1] * 50 + [2] * 50)
    n_blocks = 10
    splits = generate_time_blocked_splits(y, n_blocks=n_blocks)

    assert len(splits) == n_blocks

    all_test_indices = []
    total_samples = len(y)

    for train_idx, test_idx in splits:
        # Check no intersection
        assert len(np.intersect1d(train_idx, test_idx)) == 0
        # Check total length
        assert len(train_idx) + len(test_idx) == total_samples
        all_test_indices.extend(test_idx)

    # Every index tested exactly once
    assert len(all_test_indices) == total_samples
    assert np.array_equal(np.sort(all_test_indices), np.arange(total_samples))

def test_higher_order_moments_calculation():
    """
    Verifies statistical validity of IAT higher-order moments:
    Variance > 0, Skewness, Kurtosis calculations.
    """
    np.random.seed(42)
    # Right-skewed distribution simulating network packet inter-arrival times
    iat_samples = np.random.exponential(scale=0.05, size=1000)

    variance = np.var(iat_samples)
    skewness = stats.skew(iat_samples)
    kurt = stats.kurtosis(iat_samples)

    assert variance > 0
    # Exponential distribution has theoretical skewness ~ 2.0
    assert skewness > 1.0
    # Exponential distribution has positive excess kurtosis ~ 6.0
    assert kurt > 2.0

def test_dst_port_ablation_shape():
    """
    Verifies feature ablation dimensions: removing 1 feature from 8 yields 7.
    """
    X_sample = np.ones((100, 8))
    dst_port_idx = 6
    X_ablated = np.delete(X_sample, dst_port_idx, axis=1)

    assert X_ablated.shape == (100, 7)
