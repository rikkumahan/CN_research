"""
tests/test_composite_fitness.py
Unit tests for 5-Component Composite Fitness (Patent Claim 2):
F = alpha*f1 + beta*FRUR + gamma*CPU + delta*FSD + epsilon*BW
"""

import pytest
import numpy as np
from src.models import FFNN, DEFAULT_WEIGHTS

def test_composite_fitness_formula():
    ffnn = FFNN(ni=8, h1=16, h2=8, no=5)
    w = np.zeros(ffnn.D)
    X = np.random.randn(30, 8)
    y = np.random.randint(0, 5, size=30)

    F, f1, f2, f3, f4, f5 = ffnn.composite(X, y, w, weights=DEFAULT_WEIGHTS)

    # When w is all zeros:
    # f3 (active weights > 0.3) must be 0.0
    # f4 (FSD = mean|w| / 3.0) must be 0.0
    # f5 (BW = weights > 0.05) must be 0.0
    assert f3 == 0.0
    assert f4 == 0.0
    assert f5 == 0.0

    expected_F = (DEFAULT_WEIGHTS['alpha'] * f1 +
                  DEFAULT_WEIGHTS['beta'] * f2 +
                  DEFAULT_WEIGHTS['gamma'] * f3 +
                  DEFAULT_WEIGHTS['delta'] * f4 +
                  DEFAULT_WEIGHTS['epsilon'] * f5)
    assert np.isclose(F, expected_F, atol=1e-6)

def test_frur_noise_robustness():
    ffnn = FFNN(ni=8, h1=16, h2=8, no=5)
    w = np.random.randn(ffnn.D) * 0.5
    X = np.random.randn(50, 8)

    # FRUR should be in range [0.0, 1.0]
    frur = ffnn.f2_frur(X, w, sigma=0.10, trials=5)
    assert 0.0 <= frur <= 1.0

