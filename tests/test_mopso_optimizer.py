"""
tests/test_mopso_optimizer.py
Unit tests for MOPSO Optimizer & Page-Hinkley Drift Detector:
- Pareto dominance logic
- Archive bounding & non-dominated preservation
- Page-Hinkley error rate tracking (Claim 3)
"""

import pytest
import numpy as np
from src.mopso_optimizer import _dom, _add, _crowd, PageHinkley

def test_pareto_dominance():
    # dom(a1, a2, b1, b2): a dominates b if a <= b and strictly better in one
    assert _dom(0.1, 0.2, 0.2, 0.3) is True    # A is better in both
    assert _dom(0.1, 0.2, 0.1, 0.3) is True    # A is equal in 1st, better in 2nd
    assert _dom(0.2, 0.3, 0.1, 0.2) is False   # B is better
    assert _dom(0.1, 0.3, 0.2, 0.2) is False   # Incomparable (Trade-off)

def test_archive_management():
    # sol format: [w, f1, F, f2, f3, f4, f5]
    sol1 = [np.array([1.0]), 0.10, 0.30, 0.05, 0.5, 0.1, 0.5]
    sol2 = [np.array([2.0]), 0.20, 0.40, 0.05, 0.5, 0.1, 0.5] # Dominated by sol1
    sol3 = [np.array([3.0]), 0.05, 0.50, 0.05, 0.5, 0.1, 0.5] # Non-dominated trade-off

    arc = []
    arc = _add(arc, sol1, amax=10)
    arc = _add(arc, sol2, amax=10)
    assert len(arc) == 1  # sol2 should be rejected

    arc = _add(arc, sol3, amax=10)
    assert len(arc) == 2  # sol3 should be added

def test_page_hinkley_drift_fires_on_accuracy_drop():
    """
    Verifies that Page-Hinkley tracks error rate (1 - acc)
    and successfully fires when accuracy drops from 0.95 to 0.40.
    """
    ph = PageHinkley(delta=0.05, lam=2.0)
    
    # Phase 1: High accuracy (0.95 -> error rate 0.05)
    for _ in range(15):
        fired, val = ph.update(0.95)
        assert not fired

    # Phase 2: Drift injection - Sharp drop in accuracy (0.40 -> error rate 0.60)
    drift_detected = False
    for i in range(15):
        fired, val = ph.update(0.40)
        if fired:
            drift_detected = True
            break

    assert drift_detected is True

